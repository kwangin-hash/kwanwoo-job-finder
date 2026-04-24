package com.employment.jobfinder.ui

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.employment.jobfinder.data.JobDto

/**
 * 실질 4트랙 + 참고용 대기업 탭.
 * 로봇 관련은 배제 (자격증·스펙 핏 없음).
 */
private val TABS: List<Pair<String?, String>> = listOf(
    null to "★ 실질 타겟",
    "PUBLIC" to "공공·공기업",
    "FINANCE_DATA" to "카드·보험",
    "IT_DEV" to "중소IT 개발",
    "DATA_ANALYST" to "데이터 분석",
    "HARD" to "대기업(참고)",
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RootScreen(vm: JobViewModel) {
    var selectedTab by remember { mutableIntStateOf(0) }

    LaunchedEffect(Unit) { vm.loadHome() }
    LaunchedEffect(selectedTab) { vm.loadCategory(TABS[selectedTab].first) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("아들 취업찾기", fontWeight = FontWeight.Bold)
                        Text(
                            "현실성 점수 기준 · 청운대 CS 4학년",
                            fontSize = 11.sp,
                            color = Color.Gray,
                        )
                    }
                },
            )
        }
    ) { padding ->
        Column(Modifier.padding(padding).fillMaxSize()) {
            HomeHeader(vm)
            ScrollableTabRow(selectedTabIndex = selectedTab, edgePadding = 4.dp) {
                TABS.forEachIndexed { idx, (_, label) ->
                    Tab(
                        selected = selectedTab == idx,
                        onClick = { selectedTab = idx },
                        text = { Text(label, fontSize = 12.sp) },
                    )
                }
            }
            JobListView(vm, isHardTab = TABS[selectedTab].first == "HARD")
        }
    }
}

@Composable
private fun HomeHeader(vm: JobViewModel) {
    val state by vm.home.collectAsState()
    Column(Modifier.padding(horizontal = 12.dp, vertical = 6.dp)) {
        when {
            state.loading -> Text("요약 불러오는 중...", fontSize = 12.sp)
            state.error != null -> Text(
                state.error!!,
                color = MaterialTheme.colorScheme.error,
                fontSize = 12.sp,
            )
            else -> Row(
                Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly,
            ) {
                state.summary.forEach { s ->
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(s.label, fontSize = 11.sp)
                        Text(
                            "${s.new_today}",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.primary,
                        )
                        Text("오늘 신규 / 총 ${s.total}", fontSize = 10.sp, color = Color.Gray)
                    }
                }
            }
        }
    }
}

@Composable
private fun JobListView(vm: JobViewModel, isHardTab: Boolean) {
    val state by vm.tab.collectAsState()
    val homeState by vm.home.collectAsState()

    Column(Modifier.fillMaxSize()) {
        if (isHardTab) {
            Surface(color = Color(0xFFFFF3E0)) {
                Text(
                    "⚠ 학벌 컷이 있을 수 있는 대기업 공채입니다. 참고용으로만 확인하세요.",
                    fontSize = 11.sp,
                    modifier = Modifier.padding(12.dp),
                )
            }
        }
        when {
            state.loading -> Box(
                Modifier.fillMaxSize(), contentAlignment = Alignment.Center
            ) { CircularProgressIndicator() }
            state.error != null -> Text(
                state.error!!,
                modifier = Modifier.padding(16.dp),
                color = MaterialTheme.colorScheme.error,
            )
            state.jobs.isEmpty() -> Text(
                "공고가 없습니다.\nPC에서 서버 켜고 POST /ingest/run 을 한 번 호출해 주세요.",
                modifier = Modifier.padding(16.dp),
            )
            else -> LazyColumn(
                Modifier.fillMaxSize(),
                contentPadding = PaddingValues(8.dp),
            ) {
                items(state.jobs, key = { it.id }) { job ->
                    JobCard(job, tierLabels = homeState.tierLabels)
                }
            }
        }
    }
}

@Composable
private fun JobCard(job: JobDto, tierLabels: Map<String, String>) {
    val ctx = LocalContext.current
    ElevatedCard(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .clickable {
                ctx.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(job.url)))
            },
    ) {
        Column(Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    job.company,
                    fontWeight = FontWeight.Bold,
                    fontSize = 14.sp,
                    modifier = Modifier.weight(1f),
                )
                ScorePill("현실성 ${job.realistic_score.toInt()}", realisticColor(job.realistic_score))
            }
            Spacer(Modifier.height(4.dp))
            Text(job.title, fontSize = 14.sp)
            Spacer(Modifier.height(6.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                TierBadge(job.company_tier, tierLabels)
                Spacer(Modifier.width(6.dp))
                ScorePill("직무 ${job.match_score.toInt()}", matchColor(job.match_score))
                Spacer(Modifier.width(6.dp))
                if (job.is_entry_level == 1) {
                    ScorePill("신입", Color(0xFF1565C0))
                }
            }
            Spacer(Modifier.height(6.dp))
            Row {
                job.location?.let {
                    Text(it, fontSize = 11.sp, color = Color.Gray)
                    Spacer(Modifier.width(8.dp))
                }
                job.deadline?.let {
                    Text(
                        "마감 ~ ${it.take(10)}",
                        fontSize = 11.sp,
                        color = Color(0xFFB00020),
                    )
                }
                Spacer(Modifier.weight(1f))
                Text(job.source, fontSize = 10.sp, color = Color.Gray)
            }
        }
    }
}

@Composable
private fun TierBadge(tier: String, labels: Map<String, String>) {
    val label = labels[tier] ?: tier
    val color = when (tier) {
        "PUBLIC_LARGE", "PUBLIC_MID" -> Color(0xFF2E7D32)
        "FINANCE_IT", "CARD_INSURANCE" -> Color(0xFF1565C0)
        "SI_MID", "SME_IT", "TELCO_IT" -> Color(0xFF6A1B9A)
        "FINTECH", "ECOMMERCE", "GAME_MID" -> Color(0xFFEF6C00)
        "ROBOT_MID" -> Color(0xFFAD1457)
        "HARD" -> Color(0xFF757575)
        else -> Color(0xFF9E9E9E)
    }
    Surface(shape = MaterialTheme.shapes.small, color = color) {
        Text(
            label,
            color = Color.White,
            fontSize = 10.sp,
            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
        )
    }
}

@Composable
private fun ScorePill(text: String, color: Color) {
    Surface(shape = MaterialTheme.shapes.small, color = color) {
        Text(
            text,
            color = Color.White,
            fontSize = 10.sp,
            modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp),
        )
    }
}

private fun realisticColor(score: Double): Color = when {
    score >= 75 -> Color(0xFF2E7D32)
    score >= 55 -> Color(0xFFF9A825)
    else -> Color(0xFF9E9E9E)
}

private fun matchColor(score: Double): Color = when {
    score >= 70 -> Color(0xFF1565C0)
    score >= 50 -> Color(0xFF7E57C2)
    else -> Color(0xFF9E9E9E)
}
