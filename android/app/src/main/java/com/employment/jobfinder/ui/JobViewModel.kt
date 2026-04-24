package com.employment.jobfinder.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.employment.jobfinder.data.ApiClient
import com.employment.jobfinder.data.CategorySummaryDto
import com.employment.jobfinder.data.JobDto
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

data class TabState(
    val loading: Boolean = false,
    val jobs: List<JobDto> = emptyList(),
    val error: String? = null,
)

data class HomeState(
    val loading: Boolean = false,
    val summary: List<CategorySummaryDto> = emptyList(),
    val tierLabels: Map<String, String> = emptyMap(),
    val error: String? = null,
)

class JobViewModel : ViewModel() {
    private val _home = MutableStateFlow(HomeState())
    val home: StateFlow<HomeState> = _home.asStateFlow()

    private val _tab = MutableStateFlow(TabState())
    val tab: StateFlow<TabState> = _tab.asStateFlow()

    fun loadHome() {
        _home.value = _home.value.copy(loading = true, error = null)
        viewModelScope.launch {
            try {
                val s = ApiClient.api.summary()
                val labels = runCatching { ApiClient.api.tierLabels() }
                    .getOrDefault(emptyMap())
                _home.value = HomeState(loading = false, summary = s, tierLabels = labels)
            } catch (e: Exception) {
                _home.value = HomeState(
                    loading = false,
                    error = "서버 연결 실패: ${e.message}",
                )
            }
        }
    }

    /**
     * 탭 전환 시 호출. category == null 이면 "전체 실질 타겟" 리스트.
     * category == "HARD" 이면 참고용 대기업 공채.
     */
    fun loadCategory(category: String?) {
        _tab.value = TabState(loading = true)
        viewModelScope.launch {
            try {
                val jobs = when (category) {
                    "HARD" -> ApiClient.api.hardTierJobs()
                    null -> ApiClient.api.jobs(category = null)
                    else -> ApiClient.api.jobs(category = category)
                }
                _tab.value = TabState(loading = false, jobs = jobs)
            } catch (e: Exception) {
                _tab.value = TabState(
                    loading = false,
                    error = "불러오기 실패: ${e.message}",
                )
            }
        }
    }
}
