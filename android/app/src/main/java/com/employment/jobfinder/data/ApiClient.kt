package com.employment.jobfinder.data

import com.employment.jobfinder.BuildConfig
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import retrofit2.http.GET
import retrofit2.http.Query
import java.util.concurrent.TimeUnit

interface JobApi {
    @GET("summary")
    suspend fun summary(): List<CategorySummaryDto>

    /**
     * 실질적 합격 가능 기업 + 신입 + 대기업 제외(기본) 로 필터링 후
     * 현실성 점수 내림차순 정렬된 공고 리스트.
     */
    @GET("jobs")
    suspend fun jobs(
        @Query("category") category: String? = null,
        @Query("only_realistic") onlyRealistic: Boolean = true,
        @Query("only_entry") onlyEntry: Boolean = true,
        @Query("exclude_hard") excludeHard: Boolean = true,
        @Query("limit") limit: Int = 50,
    ): List<JobDto>

    @GET("jobs/today")
    suspend fun todayJobs(): List<JobDto>

    /** 대기업 공채 참고용 탭 */
    @GET("jobs/hard")
    suspend fun hardTierJobs(): List<JobDto>

    @GET("tier-labels")
    suspend fun tierLabels(): Map<String, String>
}

object ApiClient {
    val api: JobApi by lazy { build() }

    private fun build(): JobApi {
        val logger = HttpLoggingInterceptor().apply {
            level = HttpLoggingInterceptor.Level.BASIC
        }
        val http = OkHttpClient.Builder()
            .addInterceptor(logger)
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .build()

        val moshi = Moshi.Builder()
            .add(KotlinJsonAdapterFactory())
            .build()

        return Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .addConverterFactory(MoshiConverterFactory.create(moshi))
            .client(http)
            .build()
            .create(JobApi::class.java)
    }
}
