package com.aghnam.tikplayer

import android.annotation.SuppressLint
import android.content.res.ColorStateList
import android.view.GestureDetector
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.view.animation.OvershootInterpolator
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.ProgressBar
import android.widget.SeekBar
import android.widget.TextView
import androidx.core.view.isVisible
import androidx.media3.ui.PlayerView
import androidx.recyclerview.widget.RecyclerView
import kotlin.random.Random

class VideoAdapter(private val listener: Listener) : RecyclerView.Adapter<VideoAdapter.VH>() {

    interface Listener {
        fun onBound(holder: VH, position: Int)
        fun onRecycled(holder: VH)
        fun onTogglePlay()
        fun onLike(position: Int, holder: VH, onlyLike: Boolean)
        fun onComments(position: Int, holder: VH)
        fun onShare(position: Int, holder: VH)
        fun onSeek(fraction: Float)
    }

    val items = mutableListOf<Video>()

    @SuppressLint("NotifyDataSetChanged")
    fun submit(list: List<Video>) {
        items.clear()
        items.addAll(list)
        notifyDataSetChanged()
    }

    override fun getItemCount() = items.size

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(LayoutInflater.from(parent.context).inflate(R.layout.item_video, parent, false))

    override fun onBindViewHolder(h: VH, position: Int) {
        val v = items[position]
        h.author.text = v.author
        h.caption.text = v.caption
        h.music.text = v.music
        h.music.isSelected = true // تشغيل حركة marquee
        h.bindCounts(v)
        h.seek.progress = 0
        h.pauseIcon.isVisible = false
        h.loading.isVisible = false
        listener.onBound(h, position)
    }

    override fun onViewRecycled(holder: VH) = listener.onRecycled(holder)

    @SuppressLint("ClickableViewAccessibility")
    inner class VH(view: View) : RecyclerView.ViewHolder(view) {
        val root: FrameLayout = view.findViewById(R.id.root)
        val playerView: PlayerView = view.findViewById(R.id.playerView)
        val loading: ProgressBar = view.findViewById(R.id.loading)
        val pauseIcon: ImageView = view.findViewById(R.id.pauseIcon)
        val bigHeart: ImageView = view.findViewById(R.id.bigHeart)
        val likeBtn: ImageView = view.findViewById(R.id.likeBtn)
        val likeCount: TextView = view.findViewById(R.id.likeCount)
        val commentCount: TextView = view.findViewById(R.id.commentCount)
        val shareCount: TextView = view.findViewById(R.id.shareCount)
        val disc: View = view.findViewById(R.id.disc)
        val author: TextView = view.findViewById(R.id.author)
        val caption: TextView = view.findViewById(R.id.caption)
        val music: TextView = view.findViewById(R.id.music)
        val seek: SeekBar = view.findViewById(R.id.seek)
        var userSeeking = false

        private val pos get() = bindingAdapterPosition.takeIf { it != RecyclerView.NO_POSITION }

        init {
            val detector = GestureDetector(view.context, object : GestureDetector.SimpleOnGestureListener() {
                override fun onDown(e: MotionEvent) = true
                override fun onSingleTapConfirmed(e: MotionEvent): Boolean {
                    listener.onTogglePlay(); return true
                }
                override fun onDoubleTap(e: MotionEvent): Boolean {
                    showHeart(e.x, e.y)
                    pos?.let { listener.onLike(it, this@VH, onlyLike = true) }
                    return true
                }
            })
            root.setOnTouchListener { _, e -> detector.onTouchEvent(e) }

            likeBtn.setOnClickListener { pos?.let { listener.onLike(it, this, onlyLike = false) } }
            view.findViewById<View>(R.id.commentBtn).setOnClickListener { pos?.let { listener.onComments(it, this) } }
            view.findViewById<View>(R.id.shareBtn).setOnClickListener { pos?.let { listener.onShare(it, this) } }

            seek.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
                override fun onProgressChanged(s: SeekBar, p: Int, fromUser: Boolean) {}
                override fun onStartTrackingTouch(s: SeekBar) { userSeeking = true }
                override fun onStopTrackingTouch(s: SeekBar) {
                    listener.onSeek(s.progress / s.max.toFloat())
                    userSeeking = false
                }
            })
        }

        fun bindCounts(v: Video) {
            val color = likeBtn.context.getColor(if (v.liked) R.color.tik_red else R.color.white)
            likeBtn.imageTintList = ColorStateList.valueOf(color)
            likeCount.text = formatCount(v.likes)
            commentCount.text = formatCount(v.commentTotal)
            shareCount.text = formatCount(v.shares)
        }

        fun bounceLike() {
            likeBtn.animate().cancel()
            likeBtn.scaleX = 0.6f; likeBtn.scaleY = 0.6f
            likeBtn.animate().scaleX(1f).scaleY(1f).setStartDelay(0).setDuration(300)
                .setInterpolator(OvershootInterpolator(3f)).start()
        }

        fun showPauseIcon(show: Boolean) {
            pauseIcon.animate().cancel()
            if (!show) { pauseIcon.isVisible = false; return }
            pauseIcon.isVisible = true
            pauseIcon.scaleX = 1.6f; pauseIcon.scaleY = 1.6f
            pauseIcon.animate().scaleX(1f).scaleY(1f).setStartDelay(0).setDuration(180).start()
        }

        private fun showHeart(x: Float, y: Float) {
            val h = bigHeart
            h.animate().cancel()
            h.x = x - h.width / 2f
            h.y = y - h.height / 2f
            h.rotation = Random.nextInt(-25, 26).toFloat()
            h.scaleX = 0.3f; h.scaleY = 0.3f; h.alpha = 1f
            h.visibility = View.VISIBLE
            h.animate().scaleX(1.15f).scaleY(1.15f).setStartDelay(0).setDuration(170)
                .setInterpolator(OvershootInterpolator()).withEndAction {
                    h.animate().scaleX(1.7f).scaleY(1.7f).alpha(0f).translationYBy(-140f)
                        .setStartDelay(160).setDuration(450)
                        .withEndAction { h.visibility = View.INVISIBLE }.start()
                }.start()
        }
    }
}
