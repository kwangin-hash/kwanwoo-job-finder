package com.employment.jobfinder.data

import com.squareup.moshi.JsonClass

@JsonClass(generateAdapter = true)
data class JobDto(
    val id: Int,
    val source: String,
    val url: String,
    val company: String,
    val title: String,
    val location: String?,
    val posted_at: String?,
    val deadline: String?,

    val category: String,
    val match_score: Double,
    val realistic_score: Double,

    val company_tier: String,
    val is_target_company: Int,
    val is_hard_tier: Int,
    val is_entry_level: Int,
)

@JsonClass(generateAdapter = true)
data class CategorySummaryDto(
    val category: String,
    val label: String,
    val total: Int,
    val new_today: Int,
    val top_jobs: List<JobDto>,
)
