"""
Pillar 3 Configuration Constants
Templates and presets for voice engine, state machine, and brand integration.
"""

from typing import Dict, List, Any


# Syntax Constraints Templates
SYNTAX_CONSTRAINTS_TEMPLATES = {
    "conversational": [
        "Gunakan kalimat pendek-pendek (maksimal 12 kata per napas).",
        "Gunakan tanda kurung (...) untuk 'internal thought' atau pikiran intrusif.",
        "JANGAN gunakan tanda seru (!) untuk semangat. Gunakan hanya untuk kemarahan/kaget."
    ],
    "formal": [
        "Gunakan kalimat lengkap dengan struktur yang jelas.",
        "Hindari penggunaan slang berlebihan.",
        "Gunakan tanda baca yang tepat dan konsisten."
    ],
    "casual": [
        "Bebas gunakan kalimat pendek atau fragmen.",
        "Boleh gunakan emoji dan simbol.",
        "Santai tapi tetap terstruktur."
    ]
}


# Brand Integration Levels
BRAND_INTEGRATION_LEVELS = {
    "LEVEL_0_AMBIENT": "Produk hanya boleh disebut sebagai 'alat bantu', bukan pahlawan penyelamat hidup. Jangan hard selling.",
    "LEVEL_1_MENTION": "Produk boleh disebutkan 1x per script sebagai rekomendasi soft.",
    "LEVEL_2_SHOWCASE": "Produk menjadi bagian dari solusi yang ditawarkan (tetap natural).",
    "LEVEL_3_FEATURE": "Produk adalah fokus utama dengan demonstrasi fitur."
}


# Narrative Phases (Journey Progression)
NARRATIVE_PHASES = {
    "PHASE_1_THE_WAKE_UP_CALL": {
        "description": "Karakter baru sadar ada masalah, masih dalam denial/anger stage",
        "allowed_goals": [
            "Mengeluh tentang masalah finansial",
            "Menyadari pola tidak sehat",
            "Marah pada sistem",
            "Merasa terjebak dalam siklus"
        ],
        "forbidden_goals": [
            "Memberikan solusi finansial ahli",
            "Mengajarkan cara investasi saham",
            "Menjadi sukses tiba-tiba",
            "Sudah punya semua jawaban"
        ],
        "tone_profile": {
            "sarcasm_level": "High (8/10)",
            "optimism_level": "Low (2/10) - Masih skeptis",
            "paranoia_level": "Medium (5/10) - Curiga pada diskon"
        }
    },
    "PHASE_2_THE_EXPERIMENTATION": {
        "description": "Karakter mulai coba-coba solusi, masih trial-error",
        "allowed_goals": [
            "Mencoba tips hemat sederhana",
            "Gagal dan belajar dari kesalahan",
            "Mulai tracking pengeluaran",
            "Masih ragu tapi willing to try"
        ],
        "forbidden_goals": [
            "Langsung berhasil sempurna",
            "Jadi financial advisor dadakan",
            "Hilang semua masalah"
        ],
        "tone_profile": {
            "sarcasm_level": "Medium (5/10)",
            "optimism_level": "Medium (5/10) - Mulai ada harapan",
            "paranoia_level": "Low (3/10) - Lebih percaya diri"
        }
    },
    "PHASE_3_THE_MASTERY": {
        "description": "Karakter sudah punya sistem dan hasil terukur",
        "allowed_goals": [
            "Sharing sistem yang berhasil",
            "Celebrate small wins",
            "Membantu orang lain mulai",
            "Tetap humble tentang journey"
        ],
        "forbidden_goals": [
            "Jadi motivator toxic positivity",
            "Claim semua orang bisa kaya",
            "Lupa struggle awal"
        ],
        "tone_profile": {
            "sarcasm_level": "Low (2/10)",
            "optimism_level": "High (7/10) - Terbukti works",
            "paranoia_level": "Very Low (1/10) - Sudah confident"
        }
    }
}


# Vocabulary Blacklist (Common Violations)
COMMON_VOCABULARY_BLACKLIST = [
    # Motivator Cliche
    "Semangat Pagi",
    "Ayo Kawan",
    "Teman-teman Semua",
    "Jangan Menyerah",
    "Kamu Pasti Bisa",
    
    # Financial BS
    "Financial Freedom (terlalu jauh)",
    "Passive Income (tanpa konteks)",
    "Mindset Sukses",
    "Rich Mindset",
    "Cuan Melimpah",
    
    # Corporate Speak
    "Solusi Terbaik",
    "Kualitas Terjamin",
    "Nomor Satu",
    "Terpercaya",
    "Best in Class",
    
    # Preachy Language
    "Harus",
    "Wajib (kecuali untuk legal stuff)",
    "Kalian Perlu",
    "Dengarkan Saya",
    
    # Judging Poverty
    "Gara-gara Kopi",
    "Salah Sendiri Boros",
    "Makanya Nabung",
    "Kasian Deh Lu"
]


# Tone Modifier Presets
TONE_MODIFIER_PRESETS = {
    "rebellious": {
        "sarcasm_level": "High (8/10)",
        "optimism_level": "Low (2/10) - Masih skeptis",
        "paranoia_level": "Medium (5/10) - Curiga pada sistem"
    },
    "balanced": {
        "sarcasm_level": "Medium (5/10)",
        "optimism_level": "Medium (5/10)",
        "paranoia_level": "Low (3/10)"
    },
    "hopeful": {
        "sarcasm_level": "Low (2/10)",
        "optimism_level": "High (7/10)",
        "paranoia_level": "Very Low (1/10)"
    }
}


# Script Structure Templates (Orlic Framework Variations)
SCRIPT_STRUCTURE_TEMPLATES = {
    "standard_3_act": [
        {
            "sequence": 1,
            "type": "THE_WORLD (Hook)",
            "instruction": "Mulai dengan observasi sinis tentang status quo",
            "duration_guide": "10-15 detik"
        },
        {
            "sequence": 2,
            "type": "THE_ENEMY (Conflict)",
            "instruction": "Tunjukkan bagaimana musuh memanipulasi target",
            "duration_guide": "15-20 detik"
        },
        {
            "sequence": 3,
            "type": "THE_CHANGE (Realization)",
            "instruction": "Momen 'Glitch' - kesadaran baru",
            "duration_guide": "10-15 detik"
        }
    ],
    "extended_5_act": [
        {
            "sequence": 1,
            "type": "THE_WORLD (Hook)",
            "instruction": "Status quo yang dianggap normal",
            "duration_guide": "8-10 detik"
        },
        {
            "sequence": 2,
            "type": "THE_ENEMY (Conflict)",
            "instruction": "Musuh revealed dengan contoh konkret",
            "duration_guide": "10-12 detik"
        },
        {
            "sequence": 3,
            "type": "THE_CRISIS (Turning Point)",
            "instruction": "Moment of truth - must choose to fight or stay",
            "duration_guide": "8-10 detik"
        },
        {
            "sequence": 4,
            "type": "THE_CHANGE (Solution Glimpse)",
            "instruction": "Tunjukkan ada cara lain",
            "duration_guide": "8-10 detik"
        },
        {
            "sequence": 5,
            "type": "THE_PROMISED_LAND (Vision)",
            "instruction": "Paint the future if they join the fight",
            "duration_guide": "6-8 detik"
        }
    ]
}


# Memory Buffer Templates (Truth Terminal)
MEMORY_BUFFER_TEMPLATES = {
    "trauma_examples": [
        "Trauma: Minggu lalu gagal bayar tagihan tepat waktu.",
        "Trauma: Pernah terlilit hutang paylater sampai stress.",
        "Trauma: Ditolak saat apply kartu kredit.",
        "Trauma: Malu pas cek saldo ATM di depan teman."
    ],
    "insight_examples": [
        "Insight: Teman kantor yang gayanya hedon ternyata hutangnya banyak.",
        "Insight: Notifikasi diskon selalu muncul pas tanggal gajian.",
        "Insight: Kopi 30rb per hari = 900rb per bulan.",
        "Insight: Self-reward culture is a marketing trap."
    ],
    "realization_examples": [
        "Realization: Gaji naik tapi lifestyle juga naik (hedonic treadmill).",
        "Realization: Sistem dirancang agar kita tetap miskin.",
        "Realization: Minimalism bukan pelit, tapi rebellion.",
        "Realization: Data bisa mengalahkan FOMO."
    ]
}


# Hallucination Guidance Templates
HALLUCINATION_GUIDANCE_TEMPLATES = {
    "allowed_dystopian": "Allowed (Boleh berimajinasi tentang 'Dystopian Future' jika terus boros)",
    "allowed_utopian": "Allowed (Boleh berimajinasi tentang 'Utopian Future' jika berhasil hemat)",
    "limited_realistic": "Limited (Hanya imajinasi realistis berdasarkan data)",
    "not_allowed": "Not Allowed (Tetap pada fakta dan data saja)"
}


def get_phase_config(phase_name: str) -> Dict[str, Any]:
    """
    Get configuration for specific narrative phase
    
    Args:
        phase_name: Name of the phase (e.g., "PHASE_1_THE_WAKE_UP_CALL")
        
    Returns:
        Phase configuration dictionary
    """
    return NARRATIVE_PHASES.get(
        phase_name,
        NARRATIVE_PHASES["PHASE_1_THE_WAKE_UP_CALL"]  # Default to Phase 1
    )


def get_brand_integration_description(level: str) -> str:
    """
    Get description for brand integration level
    
    Args:
        level: Integration level key (e.g., "LEVEL_0_AMBIENT")
        
    Returns:
        Description string
    """
    return BRAND_INTEGRATION_LEVELS.get(
        level,
        BRAND_INTEGRATION_LEVELS["LEVEL_0_AMBIENT"]  # Default to ambient
    )


def get_syntax_constraints(template_name: str) -> List[str]:
    """
    Get syntax constraints for specific template
    
    Args:
        template_name: Template name (e.g., "conversational")
        
    Returns:
        List of syntax constraint strings
    """
    return SYNTAX_CONSTRAINTS_TEMPLATES.get(
        template_name,
        SYNTAX_CONSTRAINTS_TEMPLATES["conversational"]  # Default
    )


def get_tone_modifiers(preset_name: str) -> Dict[str, str]:
    """
    Get tone modifiers for specific preset
    
    Args:
        preset_name: Preset name (e.g., "rebellious")
        
    Returns:
        Tone modifier dictionary
    """
    return TONE_MODIFIER_PRESETS.get(
        preset_name,
        TONE_MODIFIER_PRESETS["rebellious"]  # Default
    )
