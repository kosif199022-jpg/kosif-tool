package com.aghnam.tikplayer

import android.Manifest
import android.animation.ObjectAnimator
import android.animation.ValueAnimator
import android.content.ContentUris
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Typeface
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.MediaStore
import android.provider.OpenableColumns
import android.view.Gravity
import android.view.View
import android.view.ViewGroup.LayoutParams.MATCH_PARENT
import android.view.ViewGroup.LayoutParams.WRAP_CONTENT
import android.view.animation.LinearInterpolator
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.annotation.OptIn
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.core.view.isVisible
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.common.VideoSize
import androidx.media3.common.util.UnstableApi
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.AspectRatioFrameLayout
import androidx.recyclerview.widget.RecyclerView
import androidx.viewpager2.widget.ViewPager2
import com.google.android.material.bottomsheet.BottomSheetDialog

@OptIn(UnstableApi::class)
class MainActivity : AppCompatActivity(), VideoAdapter.Listener {

    private enum class Tab { FOR_YOU, MINE }

    private lateinit var pager: ViewPager2
    private lateinit var emptyView: TextView
    private lateinit var player: ExoPlayer
    private val adapter = VideoAdapter(this)

    private val forYou = Samples.list()
    private val mine = mutableListOf<Video>()
    private var tab = Tab.FOR_YOU

    /** الصفحة التي يعمل عليها المشغل الآن، والـ ViewHolder المرتبط بها */
    private var currentPos = RecyclerView.NO_POSITION
    private var current: VideoAdapter.VH? = null
    private var userPaused = false
    private var discAnim: ObjectAnimator? = null

    private val ui = Handler(Looper.getMainLooper())
    private val prefs by lazy { getSharedPreferences("tikplayer", MODE_PRIVATE) }

    private val progressTick = object : Runnable {
        override fun run() {
            updateProgress()
            ui.postDelayed(this, 200)
        }
    }

    private val pickVideos =
        registerForActivityResult(ActivityResultContracts.OpenMultipleDocuments()) { uris ->
            if (uris.isEmpty()) return@registerForActivityResult
            val saved = prefs.getStringSet(KEY_PICKED, emptySet())!!.toMutableSet()
            uris.forEach { uri ->
                runCatching {
                    contentResolver.takePersistableUriPermission(uri, Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                saved.add(uri.toString())
            }
            prefs.edit().putStringSet(KEY_PICKED, saved).apply()
            mine.removeAll { v -> v.uri in uris }
            mine.addAll(0, uris.map { localVideo(it, displayName(it)) })
            showTab(Tab.MINE)
        }

    private val askPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { granted ->
            if (granted) loadDeviceVideos()
        }

    private val playerListener = object : Player.Listener {
        override fun onVideoSizeChanged(videoSize: VideoSize) = applyResize(videoSize)

        override fun onPlaybackStateChanged(state: Int) {
            current?.loading?.isVisible = state == Player.STATE_BUFFERING
        }

        override fun onIsPlayingChanged(isPlaying: Boolean) {
            discAnim?.let { if (isPlaying) it.resume() else it.pause() }
        }

        override fun onPlayerError(error: PlaybackException) {
            current?.loading?.isVisible = false
            Toast.makeText(this@MainActivity, "تعذّر تشغيل هذا الفيديو", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        pager = findViewById(R.id.pager)
        emptyView = findViewById(R.id.empty)

        player = ExoPlayer.Builder(this).build().apply {
            repeatMode = Player.REPEAT_MODE_ONE
            addListener(playerListener)
        }

        pager.adapter = adapter
        pager.offscreenPageLimit = 1
        pager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) = playAt(position)
        })

        findViewById<View>(R.id.tabForYou).setOnClickListener { showTab(Tab.FOR_YOU) }
        findViewById<View>(R.id.tabMine).setOnClickListener { showTab(Tab.MINE) }
        findViewById<View>(R.id.addBtn).setOnClickListener { pickVideos.launch(arrayOf("video/*")) }

        loadPickedVideos()
        if (hasVideoPermission()) loadDeviceVideos()
        if (!handleViewIntent(intent)) showTab(Tab.FOR_YOU)
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handleViewIntent(intent)
    }

    override fun onStart() {
        super.onStart()
        ui.post(progressTick)
        if (!userPaused && currentPos != RecyclerView.NO_POSITION) player.play()
    }

    override fun onStop() {
        super.onStop()
        ui.removeCallbacks(progressTick)
        player.pause()
    }

    override fun onDestroy() {
        super.onDestroy()
        discAnim?.cancel()
        player.release()
    }

    // ---------- التبويبات والقوائم ----------

    private fun showTab(t: Tab) {
        tab = t
        val white = getColor(R.color.white)
        val dim = getColor(R.color.dim_white)
        findViewById<TextView>(R.id.tabForYouText).setTextColor(if (t == Tab.FOR_YOU) white else dim)
        findViewById<TextView>(R.id.tabMineText).setTextColor(if (t == Tab.MINE) white else dim)
        findViewById<View>(R.id.tabForYouLine).visibility = if (t == Tab.FOR_YOU) View.VISIBLE else View.INVISIBLE
        findViewById<View>(R.id.tabMineLine).visibility = if (t == Tab.MINE) View.VISIBLE else View.INVISIBLE

        if (t == Tab.MINE && !hasVideoPermission()) askPermission.launch(videoPermission())

        current?.let { detach(it) }
        currentPos = RecyclerView.NO_POSITION
        val list = if (t == Tab.FOR_YOU) forYou else mine
        adapter.submit(list)
        emptyView.isVisible = list.isEmpty()
        if (list.isEmpty()) {
            player.stop()
            player.clearMediaItems()
            return
        }
        pager.setCurrentItem(0, false)
        pager.post { playAt(pager.currentItem) }
    }

    /** يحدّث قائمة "فيديوهاتي" إن كانت ظاهرة دون أن يقطع الفيديو الحالي */
    private fun refreshMine() {
        if (tab != Tab.MINE) return
        if (adapter.items.isEmpty()) { showTab(Tab.MINE); return }
        adapter.submit(mine)
        emptyView.isVisible = mine.isEmpty()
    }

    private fun handleViewIntent(intent: Intent?): Boolean {
        val uri = intent?.data ?: return false
        if (intent.action != Intent.ACTION_VIEW) return false
        mine.removeAll { it.uri == uri }
        mine.add(0, localVideo(uri, displayName(uri)))
        showTab(Tab.MINE)
        return true
    }

    private fun localVideo(uri: Uri, name: String) = Video(
        uri = uri,
        author = "@أنا",
        caption = name.substringBeforeLast('.'),
        music = "الصوت الأصلي - $name",
        isLocal = true,
    )

    private fun displayName(uri: Uri): String {
        runCatching {
            contentResolver.query(uri, arrayOf(OpenableColumns.DISPLAY_NAME), null, null, null)?.use { c ->
                if (c.moveToFirst()) c.getString(0)?.let { return it }
            }
        }
        return uri.lastPathSegment ?: "فيديو"
    }

    private fun loadPickedVideos() {
        val persisted = contentResolver.persistedUriPermissions.map { it.uri }.toSet()
        prefs.getStringSet(KEY_PICKED, emptySet())!!
            .map(Uri::parse)
            .filter { it in persisted }
            .forEach { mine.add(localVideo(it, displayName(it))) }
    }

    private fun videoPermission() =
        if (Build.VERSION.SDK_INT >= 33) Manifest.permission.READ_MEDIA_VIDEO
        else Manifest.permission.READ_EXTERNAL_STORAGE

    private fun hasVideoPermission() =
        ContextCompat.checkSelfPermission(this, videoPermission()) == PackageManager.PERMISSION_GRANTED

    private fun loadDeviceVideos() {
        Thread {
            val found = mutableListOf<Video>()
            val collection = MediaStore.Video.Media.EXTERNAL_CONTENT_URI
            val projection = arrayOf(MediaStore.Video.Media._ID, MediaStore.Video.Media.DISPLAY_NAME)
            runCatching {
                contentResolver.query(
                    collection, projection, null, null,
                    "${MediaStore.Video.Media.DATE_ADDED} DESC",
                )?.use { c ->
                    val idCol = c.getColumnIndexOrThrow(MediaStore.Video.Media._ID)
                    val nameCol = c.getColumnIndexOrThrow(MediaStore.Video.Media.DISPLAY_NAME)
                    while (c.moveToNext() && found.size < 500) {
                        val uri = ContentUris.withAppendedId(collection, c.getLong(idCol))
                        found += localVideo(uri, c.getString(nameCol) ?: "فيديو")
                    }
                }
            }
            runOnUiThread {
                val existing = mine.map { it.uri }.toSet()
                mine.addAll(found.filter { it.uri !in existing })
                refreshMine()
            }
        }.start()
    }

    // ---------- التشغيل ----------

    private fun playAt(position: Int) {
        if (position !in adapter.items.indices || position == currentPos) return
        current?.let { detach(it) }
        currentPos = position
        userPaused = false
        player.setMediaItem(MediaItem.fromUri(adapter.items[position].uri))
        player.prepare()
        player.playWhenReady = true
        holderAt(position)?.let { attach(it) } // وإلا يُربط عند onBound
    }

    private fun holderAt(position: Int): VideoAdapter.VH? =
        (pager.getChildAt(0) as? RecyclerView)?.findViewHolderForAdapterPosition(position) as? VideoAdapter.VH

    private fun attach(h: VideoAdapter.VH) {
        if (current === h) return
        current?.let { detach(it) }
        current = h
        h.playerView.player = player
        h.showPauseIcon(false)
        h.loading.isVisible = player.playbackState == Player.STATE_BUFFERING
        applyResize(player.videoSize)
        discAnim = ObjectAnimator.ofFloat(h.disc, View.ROTATION, 0f, 360f).apply {
            duration = 4000
            repeatCount = ValueAnimator.INFINITE
            interpolator = LinearInterpolator()
            start()
            if (!player.isPlaying) pause()
        }
    }

    private fun detach(h: VideoAdapter.VH) {
        h.playerView.player = null
        h.showPauseIcon(false)
        h.loading.isVisible = false
        h.seek.progress = 0
        if (current === h) {
            discAnim?.cancel()
            discAnim = null
            h.disc.rotation = 0f
            current = null
        }
    }

    private fun applyResize(size: VideoSize) {
        val h = current ?: return
        if (size.width == 0 || size.height == 0) return
        // الفيديو العمودي يملأ الشاشة مثل تيك توك، والأفقي يظهر كاملاً
        h.playerView.resizeMode =
            if (size.height > size.width) AspectRatioFrameLayout.RESIZE_MODE_ZOOM
            else AspectRatioFrameLayout.RESIZE_MODE_FIT
    }

    private fun updateProgress() {
        val h = current ?: return
        if (h.userSeeking) return
        val duration = player.duration
        if (duration > 0) h.seek.progress = (player.currentPosition * h.seek.max / duration).toInt()
    }

    // ---------- أحداث الواجهة ----------

    override fun onBound(holder: VideoAdapter.VH, position: Int) {
        if (position == currentPos) attach(holder)
        else if (holder === current) detach(holder)
    }

    override fun onRecycled(holder: VideoAdapter.VH) {
        if (holder === current) detach(holder)
    }

    override fun onTogglePlay() {
        val h = current ?: return
        if (player.isPlaying) {
            player.pause()
            userPaused = true
            h.showPauseIcon(true)
        } else {
            if (player.playbackState == Player.STATE_IDLE) player.prepare()
            player.play()
            userPaused = false
            h.showPauseIcon(false)
        }
    }

    override fun onLike(position: Int, holder: VideoAdapter.VH, onlyLike: Boolean) {
        val v = adapter.items.getOrNull(position) ?: return
        if (onlyLike && v.liked) return
        v.liked = !v.liked
        v.likes += if (v.liked) 1 else -1
        holder.bindCounts(v)
        holder.bounceLike()
    }

    override fun onSeek(fraction: Float) {
        val duration = player.duration
        if (duration > 0) player.seekTo((duration * fraction).toLong())
    }

    override fun onShare(position: Int, holder: VideoAdapter.VH) {
        val v = adapter.items.getOrNull(position) ?: return
        val send = Intent(Intent.ACTION_SEND).apply {
            if (v.isLocal) {
                type = "video/*"
                putExtra(Intent.EXTRA_STREAM, v.uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            } else {
                type = "text/plain"
                putExtra(Intent.EXTRA_TEXT, "${v.caption}\n${v.uri}")
            }
        }
        startActivity(Intent.createChooser(send, getString(R.string.share_via)))
        v.shares++
        holder.bindCounts(v)
    }

    override fun onComments(position: Int, holder: VideoAdapter.VH) {
        val v = adapter.items.getOrNull(position) ?: return
        val dp = resources.displayMetrics.density
        fun px(n: Int) = (n * dp).toInt()
        val white = getColor(R.color.white)
        val dim = getColor(R.color.dim_white)

        val title = TextView(this).apply {
            setTextColor(white); textSize = 15f; typeface = Typeface.DEFAULT_BOLD
            gravity = Gravity.CENTER; setPadding(0, px(4), 0, px(12))
        }
        val list = LinearLayout(this).apply { orientation = LinearLayout.VERTICAL }
        fun render() {
            title.text = "${getString(R.string.comments)} (${formatCount(v.commentTotal)})"
            list.removeAllViews()
            v.comments.forEach { c ->
                list.addView(TextView(this).apply {
                    text = c; setTextColor(white); textSize = 14f; setPadding(0, px(10), 0, px(10))
                })
            }
        }
        val input = EditText(this).apply {
            hint = getString(R.string.add_comment)
            setTextColor(white); setHintTextColor(dim); textSize = 14f
        }
        val send = TextView(this).apply {
            text = getString(R.string.send)
            setTextColor(getColor(R.color.tik_red)); typeface = Typeface.DEFAULT_BOLD
            setPadding(px(14), px(10), px(4), px(10))
            setOnClickListener {
                val text = input.text.toString().trim()
                if (text.isEmpty()) return@setOnClickListener
                v.comments.add("@أنا: $text")
                input.text.clear()
                render()
                if (holder.bindingAdapterPosition == position) holder.bindCounts(v)
            }
        }
        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            addView(input, LinearLayout.LayoutParams(0, WRAP_CONTENT, 1f))
            addView(send)
        }
        val sheet = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(getColor(R.color.sheet_bg))
            setPadding(px(16), px(14), px(16), px(10))
            addView(title, MATCH_PARENT, WRAP_CONTENT)
            addView(ScrollView(this@MainActivity).apply { addView(list) }, MATCH_PARENT, px(340))
            addView(row, MATCH_PARENT, WRAP_CONTENT)
        }
        render()
        BottomSheetDialog(this).apply { setContentView(sheet); show() }
    }

    companion object {
        private const val KEY_PICKED = "picked_uris"
    }
}
