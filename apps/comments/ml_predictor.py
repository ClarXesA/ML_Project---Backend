def predict_sentiment(text: str) -> bool | None:
    """
    Placeholder untuk integrasi model ML.
    Diharapkan mengembalikan:
    - True untuk sentimen positif
    - False untuk negatif
    - None jika tidak bisa diproses
    """
    # Logika ML palsu:
    # Untuk sekarang, kita anggap komentar yang mengandung "jelek"
    # adalah negatif, sisanya positif.
    if "jelek" in text.lower():
        return False
    
    # Default, anggap positif
    return True