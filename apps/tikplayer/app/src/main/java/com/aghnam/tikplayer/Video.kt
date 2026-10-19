package com.aghnam.tikplayer

import android.net.Uri
import java.util.Locale

data class Video(
    val uri: Uri,
    val author: String,
    val caption: String,
    val music: String,
    var likes: Int = 0,
    var liked: Boolean = false,
    /** عدد تعليقات وهمي يُضاف للعدّاد ليشبه المحتوى الحقيقي */
    val baseComments: Int = 0,
    val comments: MutableList<String> = mutableListOf(),
    var shares: Int = 0,
    val isLocal: Boolean = false,
) {
    val commentTotal get() = baseComments + comments.size
}

fun formatCount(n: Int): String = when {
    n >= 1_000_000 -> String.format(Locale.US, "%.1fM", n / 1_000_000f).replace(".0M", "M")
    n >= 10_000 -> "${n / 1000}K"
    n >= 1_000 -> String.format(Locale.US, "%.1fK", n / 1000f).replace(".0K", "K")
    else -> n.toString()
}

object Samples {
    private const val BASE = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/"

    private val seedComments = listOf(
        "@sara: رووعة 😍",
        "@ahmed: من وين هذا المكان؟",
        "@noor: أحلى فيديو اليوم 🔥",
        "@khalid: كمّل كمّل 👏",
    )

    fun list(): List<Video> = listOf(
        Triple("ForBiggerBlazes.mp4", "@blaze.tv", "لحظات حماسية 🔥 #لك #fyp"),
        Triple("ForBiggerEscapes.mp4", "@escape", "هروب من الروتين 🏞️ #سفر"),
        Triple("ForBiggerFun.mp4", "@fun.zone", "ضحك من القلب 😂 #ترند"),
        Triple("ForBiggerJoyrides.mp4", "@joyride", "جولة ولا أروع 🚗 #سيارات"),
        Triple("ForBiggerMeltdowns.mp4", "@meltdown", "لما يخلص الشحن 😅 #كوميدي"),
        Triple("SubaruOutbackOnStreetAndDirt.mp4", "@offroad", "طريق ترابي ومغامرة 🏔️ #مغامرة"),
        Triple("BigBuckBunny.mp4", "@bunny", "الأرنب الكبير 🐰 #أنمي"),
        Triple("ElephantsDream.mp4", "@dreams", "حلم الفيلة 🐘 #فن"),
        Triple("TearsOfSteel.mp4", "@scifi", "دموع الفولاذ 🤖 #خيال_علمي"),
    ).mapIndexed { i, (file, author, caption) ->
        Video(
            uri = Uri.parse(BASE + file),
            author = author,
            caption = caption,
            music = "الصوت الأصلي - ${author.drop(1)}",
            likes = 1200 + i * 48_731 % 900_000,
            baseComments = 40 + i * 317,
            comments = seedComments.shuffled().take(2 + i % 3).toMutableList(),
            shares = 30 + i * 91,
        )
    }
}
