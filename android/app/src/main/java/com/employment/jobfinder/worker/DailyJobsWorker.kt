package com.employment.jobfinder.worker

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.os.Build
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import androidx.work.*
import com.employment.jobfinder.R
import com.employment.jobfinder.data.ApiClient
import java.util.Calendar
import java.util.concurrent.TimeUnit

/**
 * 매일 아침 07:00 에 서버에서 오늘의 신규 공고 Top 5 를 받아와 알림 표시.
 */
class DailyJobsWorker(
    ctx: Context,
    params: WorkerParameters,
) : CoroutineWorker(ctx, params) {

    override suspend fun doWork(): Result {
        return try {
            val jobs = ApiClient.api.todayJobs().take(5)
            if (jobs.isNotEmpty()) notify(jobs)
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }

    private fun notify(jobs: List<com.employment.jobfinder.data.JobDto>) {
        val ctx = applicationContext
        ensureChannel(ctx)

        val text = jobs.joinToString("\n") {
            "- [${it.match_score.toInt()}] ${it.company} · ${it.title}"
        }
        val notif = NotificationCompat.Builder(ctx, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle("오늘의 추천 공고 ${jobs.size}건")
            .setStyle(NotificationCompat.BigTextStyle().bigText(text))
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .build()

        runCatching {
            NotificationManagerCompat.from(ctx).notify(NOTIF_ID, notif)
        }
    }

    private fun ensureChannel(ctx: Context) {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.O) return
        val mgr = ctx.getSystemService(Context.NOTIFICATION_SERVICE)
                as NotificationManager
        if (mgr.getNotificationChannel(CHANNEL_ID) == null) {
            mgr.createNotificationChannel(
                NotificationChannel(
                    CHANNEL_ID,
                    "매일 취업 공고",
                    NotificationManager.IMPORTANCE_DEFAULT,
                )
            )
        }
    }

    companion object {
        private const val CHANNEL_ID = "daily_jobs"
        private const val NOTIF_ID = 1001
        private const val WORK_NAME = "daily_jobs_worker"

        fun schedule(ctx: Context) {
            val initialDelay = computeDelayUntil7am()
            val req = PeriodicWorkRequestBuilder<DailyJobsWorker>(
                1, TimeUnit.DAYS
            )
                .setInitialDelay(initialDelay, TimeUnit.MILLISECONDS)
                .setConstraints(
                    Constraints.Builder()
                        .setRequiredNetworkType(NetworkType.CONNECTED)
                        .build()
                )
                .build()

            WorkManager.getInstance(ctx).enqueueUniquePeriodicWork(
                WORK_NAME,
                ExistingPeriodicWorkPolicy.UPDATE,
                req,
            )
        }

        private fun computeDelayUntil7am(): Long {
            val now = Calendar.getInstance()
            val next = Calendar.getInstance().apply {
                set(Calendar.HOUR_OF_DAY, 7)
                set(Calendar.MINUTE, 0)
                set(Calendar.SECOND, 0)
                if (before(now)) add(Calendar.DAY_OF_MONTH, 1)
            }
            return next.timeInMillis - now.timeInMillis
        }
    }
}
