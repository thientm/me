import random

TAMANLAC_TEMPLATES = [
    "Nam Mô A Di Đà Phật, chúc đạo hữu và gia đình luôn an lạc, vạn sự cát tường 🙏",
    "Tâm An Lạc kính chúc quý bạn thân tâm thanh tịnh, mọi sự hanh thông an lành 🙏",
    "Kính chúc đạo hữu một ngày nhẹ nhàng, an vui trong ánh sáng từ bi 🙏",
    "Cảm ơn đạo hữu đã lắng nghe và đồng hành cùng Tâm An Lạc. Chúc bạn vạn sự bình an 🙏",
    "Nguyện chúc quý bạn và gia quyến luôn được che chở trong an lành và hoan hỷ 🙏",
    "Nam Mô Quán Thế Âm Bồ Tát, chúc bạn luôn giữ được sự an nhiên trong tâm hồn 🙏",
    "Biết ơn mối duyên lành này. Kính chúc đạo hữu một ngày an vui, tĩnh tại 🙏",
    "Chúc bạn một ngày trọn vẹn bình yên và nhiều năng lượng thiện lành 🙏"
]

METECH_TEMPLATES = [
    "Cảm ơn bạn nhiều nha! Nhớ đón xem các video AI và công nghệ tiếp theo của kênh nhé 🔥",
    "Cảm ơn bạn đã ủng hộ Mê Tech! Chúc bạn ứng dụng AI vào công việc thật hiệu quả 🚀",
    "Cảm ơn bạn! Đừng quên theo dõi kênh để không bỏ lỡ tin công nghệ mới mỗi ngày nha ✨",
    "Mê Tech cảm ơn bạn rất nhiều! Chúc bạn một ngày làm việc tràn đầy cảm hứng 💡",
    "Rất vui vì thông tin hữu ích với bạn. Hẹn bạn ở các video tiếp theo nhé! 🙌",
    "Cảm ơn bạn đã đồng hành cùng Mê Tech! 🚀"
]

def get_template_reply(channel: str, category: str, author: str = "") -> str:
    if channel == "tamanlac":
        return random.choice(TAMANLAC_TEMPLATES)
    else:
        return random.choice(METECH_TEMPLATES)
