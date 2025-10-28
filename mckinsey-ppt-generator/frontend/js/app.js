/**
 * McKinsey PPT Generator - 메인 애플리케이션 로직
 */

// 전역 변수
let currentStep = 1;
let currentPPTId = null;
let pollInterval = null;
let currentProjectId = null;

// 파일 업로드 관련 변수
let uploadedText = '';
let currentFile = null;

// 단계 설명
const stageDescriptions = {
    'document_analysis': 'AI가 비즈니스 문서를 분석하고 있습니다',
    'structure_design': 'McKinsey MECE 구조를 설계하고 있습니다',
    'content_generation': '헤드라인과 인사이트를 생성하고 있습니다',
    'design_application': '전문적인 디자인을 적용하고 있습니다',
    'quality_review': '품질을 검토하고 최적화하고 있습니다'
};

// DOM 요소
const elements = {
    documentInput: document.getElementById('documentInput'),
    charCount: document.getElementById('charCount'),
    nextToOptions: document.getElementById('nextToOptions'),
    backToDocument: document.getElementById('backToDocument'),
    generatePPT: document.getElementById('generatePPT'),
    styleSelect: document.getElementById('styleSelect'),
    audienceSelect: document.getElementById('audienceSelect'),
    numSlidesRange: document.getElementById('numSlidesRange'),
    numSlidesValue: document.getElementById('numSlidesValue'),
    languageSelect: document.getElementById('languageSelect'),
    progressBar: document.getElementById('progressBar'),
    currentStage: document.getElementById('currentStage'),
    stageDescription: document.getElementById('stageDescription'),
    qualityScore: document.getElementById('qualityScore'),
    scoreValue: document.getElementById('scoreValue'),
    generationTime: document.getElementById('generationTime'),
    downloadPPT: document.getElementById('downloadPPT'),
    createNew: document.getElementById('createNew'),
    // 파일 업로드 관련 요소
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    selectFileBtn: document.getElementById('selectFileBtn'),
    removeFileBtn: document.getElementById('removeFileBtn'),
    uploadProgress: document.getElementById('uploadProgress'),
    progressFill: document.getElementById('progressFill'),
    uploadStatus: document.getElementById('uploadStatus'),
    fileInfo: document.getElementById('fileInfo'),
    fileName: document.getElementById('fileName'),
    fileSize: document.getElementById('fileSize'),
    previewText: document.getElementById('previewText'),
    textTab: document.getElementById('text-tab'),
    fileTab: document.getElementById('file-tab'),
    textInputPane: document.getElementById('text-input'),
    fileUploadPane: document.getElementById('file-upload')
};

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkAPIHealth();
    initFileUpload(); // 파일 업로드 초기화 추가
});

/**
 * 앱 초기화
 */
function initializeApp() {
    console.log('McKinsey PPT Generator 초기화...');
    updateNextButton(); // 초기 버튼 상태 업데이트
}

/**
 * 이벤트 리스너 설정
 */
function setupEventListeners() {
    // 문서 입력 카운터
    elements.documentInput.addEventListener('input', updateNextButton);

    // 슬라이드 수 슬라이더
    elements.numSlidesRange.addEventListener('input', () => {
        elements.numSlidesValue.textContent = elements.numSlidesRange.value;
    });

    // 단계 이동 버튼
    elements.nextToOptions.addEventListener('click', moveToStep2);
    elements.backToDocument.addEventListener('click', () => goToStep(1));
    elements.generatePPT.addEventListener('click', startGeneration);
    elements.downloadPPT.addEventListener('click', downloadPPTFile);
    elements.createNew.addEventListener('click', () => location.reload());

    // 탭 전환 시 다음 버튼 상태 업데이트
    elements.textTab.addEventListener('shown.bs.tab', updateNextButton);
    elements.fileTab.addEventListener('shown.bs.tab', updateNextButton);

    // 단계별 모드 토글 및 버튼
    const toggle = document.getElementById('phaseModeToggle');
    const btnA = document.getElementById('btnPhaseAnalyze');
    const btnS = document.getElementById('btnPhaseStructure');
    const btnC = document.getElementById('btnPhaseContent');
    const btnD = document.getElementById('btnPhaseDesign');
    const btnR = document.getElementById('btnPhaseReview');
    const btnE = document.getElementById('btnPhaseExport');
    const phaseLog = document.getElementById('phaseLog');

    if (toggle) {
        toggle.addEventListener('change', () => {
           // 단순 토글 표시만 처리 (실행 경로는 startGeneration에서 분기)
        });
    }
    function appendLog(obj){
        try { phaseLog.textContent += (typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2)) + "\n"; }
        catch(e){ phaseLog.textContent += String(obj) + "\n"; }
        phaseLog.scrollTop = phaseLog.scrollHeight;
    }
    function renderAnalyzeResult(res){
        const panel = document.getElementById('analyzePanel');
        const coreMsg = document.getElementById('coreMessage');
        const dpCount = document.getElementById('dataPointCount');
        const topicsSpan = document.getElementById('keyTopics');
        const topicsList = document.getElementById('keyTopicsList');
        try{
            const result = (res && res.result) ? res.result : res;
            const core = result.core_message || result.key_message || '-';
            coreMsg.textContent = core.length>140? (core.substring(0,140)+'...') : core;
            const dps = result.data_points || [];
            dpCount.textContent = dps.length || 0;
            // Normalize key_topics into an array of strings for robust rendering
            let ktRaw = (result && result.key_topics !== undefined) ? result.key_topics : [];
            let ktArr = [];
            if (Array.isArray(ktRaw)) {
                ktArr = ktRaw.map(x => (x == null ? '' : String(x))).filter(Boolean);
            } else if (typeof ktRaw === 'string') {
                ktArr = ktRaw
                    .split(/[\n,\u2022\u2023\u25E6\u2043\u2219]/) // split by commas, newlines, common bullet chars
                    .map(s => s.trim())
                    .filter(Boolean);
            } else if (ktRaw && typeof ktRaw === 'object') {
                // If it's an object (e.g., {0: 'A', 1: 'B'}), coerce values
                try { ktArr = Object.values(ktRaw).map(x => String(x)).filter(Boolean); } catch(e) { ktArr = []; }
            }
            // Render to bullet list if present, keep span fallback for compatibility
            if (topicsList) {
                if (ktArr.length === 0) {
                    topicsList.innerHTML = '<li class="text-muted">-</li>';
                } else {
                    topicsList.innerHTML = '';
                    ktArr.forEach(t => {
                        const li = document.createElement('li');
                        li.textContent = t;
                        topicsList.appendChild(li);
                    });
                }
            }
            if (topicsSpan) {
                topicsSpan.textContent = (ktArr && ktArr.length) ? ktArr.join(', ') : '-';
            }
            panel.style.display = '';
        }catch(e){ /* ignore UI errors */ }
    }
    function renderStructureResult(res){
        const panel = document.getElementById('structurePanel');
        const list = document.getElementById('slideOutline');
        list.innerHTML='';
        try{
            const result = (res && res.result) ? res.result : res;
            const outline = result.slide_outline || [];
            outline.slice(0,20).forEach(it=>{
                const li = document.createElement('li');
                li.className='list-group-item';
                li.textContent = `${it.slide_number}. [${it.type}] ${it.content_focus || ''}`;
                list.appendChild(li);
            });
            panel.style.display = '';
        }catch(e){ /* ignore */ }
    }
    // 각 단계 버튼
    if (btnA) btnA.addEventListener('click', async ()=>{ await runSinglePhase('analyze'); });
    if (btnS) btnS.addEventListener('click', async ()=>{ await runSinglePhase('structure'); });
    if (btnC) btnC.addEventListener('click', async ()=>{ await runSinglePhase('content'); });
    if (btnD) btnD.addEventListener('click', async ()=>{ await runSinglePhase('design'); });
    if (btnR) btnR.addEventListener('click', async ()=>{ await runSinglePhase('review'); });
    if (btnE) btnE.addEventListener('click', async ()=>{ await runSinglePhase('export'); });
    
    async function runSinglePhase(phase){
        try{
            if(!window.appState || !window.appState.document){
                showAlert('문서를 먼저 입력/업로드하세요.', 'warning');
                return;
            }
            if(!currentProjectId) currentProjectId = guid();
            const payload = {
               project_id: currentProjectId,
               document: window.appState.document,
               num_slides: parseInt(elements.numSlidesRange.value),
               language: elements.languageSelect.value
            };
            // UI: 진행률/체크리스트 갱신
            const stageKeyMap = { analyze: 'document_analysis', structure: 'structure_design', content: 'content_generation', design: 'design_application', review: 'quality_review' };
            const progressMap = { analyze: 10, structure: 30, content: 50, design: 70, review: 90, export: 100 };
            const stageNameText = { analyze: '분석(Phase 1)', structure: '구조설계(Phase 2)', content: '콘텐츠생성(Phase 3)', design: '디자인(Phase 4)', review: '리뷰(Phase 5)', export: '내보내기' };
            updateProgress(progressMap[phase] || 0);
            elements.currentStage.textContent = stageNameText[phase] || '진행 중';
            if (stageKeyMap[phase]) { try { updateStageChecklist(stageKeyMap[phase]); } catch(e) {} }

            let res;
            if(phase==='analyze') { res = await api.analyze(payload); appendLog({phase, res}); renderAnalyzeResult(res); }
            if(phase==='structure') { res = await api.structure(payload); appendLog({phase, res}); renderStructureResult(res); }
            if(phase==='content') { res = await api.content(payload); appendLog({phase, res}); }
            if(phase==='design') { res = await api.design(payload); appendLog({phase, res}); }
            if(phase==='review') { res = await api.review(payload); appendLog({phase, res}); }
            if(phase==='export') { res = await api.export(payload); appendLog({phase, res}); }

            // 실패 처리
            const statusVal = (res && res.status) || (res && res.res && res.res.status);
            const errorVal = (res && res.error) || (res && res.res && res.res.error);
            if ((statusVal && statusVal !== 'completed') || errorVal) {
                showAlert(`단계 실패(${phase}): ${errorVal || statusVal}`, 'danger');
                return;
            }
            if(phase==='export'){
               if(res && res.result && res.result.pptx_path){
                   updateProgress(100);
                   elements.currentStage.textContent = '완료';
                   elements.qualityScore.classList.remove('d-none');
                   elements.scoreValue.textContent = (res.result.quality_score || 0).toFixed(3);
               }else{
                   showAlert('내보내기 실패: '+ (res && res.error ? res.error : '원인 불명'), 'danger');
               }
            } else {
                // 자동 진행: 단계별 모드 토글 시 다음 단계로 체인 실행
                const chain = ['analyze','structure','content','design','review','export'];
                const curIdx = chain.indexOf(phase);
                if (toggle && toggle.checked && curIdx >= 0 && curIdx < chain.length - 1) {
                    await runSinglePhase(chain[curIdx + 1]);
                }
            }
        }catch(e){
            appendLog({phase, error: e && e.message ? e.message : String(e)});
            showAlert('단계 실행 중 오류: '+ (e&&e.message?e.message:String(e)), 'danger');
        }
    }
}

/**
 * API 헬스 체크
 */
async function checkAPIHealth() {
    try {
        const health = await api.healthCheck();
        if (health.status === 'healthy') {
            console.log('✅ API 서버 정상 작동');
        } else {
            showAlert('경고: API 서버 상태를 확인할 수 없습니다', 'warning');
        }
    } catch (error) {
        showAlert('오류: API 서버에 연결할 수 없습니다', 'danger');
    }
}

/**
 * 다음 버튼 상태 업데이트
 */
function updateNextButton() {
    const textInput = elements.documentInput.value.trim();
    const hasTextInput = textInput.length >= 100;
    const hasUploadedFile = uploadedText.length > 0; // 파일이 업로드되어 텍스트가 추출되었는지 확인

    // 텍스트 입력 탭이 활성화되어 있고 텍스트가 충분하거나,
    // 파일 업로드 탭이 활성화되어 있고 파일이 업로드되어 텍스트가 추출된 경우
    const isTextTabActive = elements.textInputPane.classList.contains('show');
    const isFileTabActive = elements.fileUploadPane.classList.contains('show');

    if (isTextTabActive) {
        elements.nextToOptions.disabled = !hasTextInput;
        elements.charCount.textContent = textInput.length;
        elements.charCount.style.color = hasTextInput ? '#6BA644' : '#53565A';
    } else if (isFileTabActive) {
        elements.nextToOptions.disabled = !hasUploadedFile;
    }
}

/**
 * 단계 이동
 */
function goToStep(step) {
    // 현재 단계 비활성화
    document.querySelector(`#step-${currentStep}`).classList.remove('active');
    document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');

    // 새 단계 활성화
    currentStep = step;
    document.querySelector(`#step-${currentStep}`).classList.add('active');
    document.querySelector(`.step[data-step="${currentStep}"]`).classList.add('active');

    // 이전 단계 완료 표시
    for (let i = 1; i < currentStep; i++) {
        document.querySelector(`.step[data-step="${i}"]`).classList.add('completed');
    }

    // 페이지 상단으로 스크롤
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Step 1 → Step 2 이동
 */
function moveToStep2() {
    let documentContent = '';
    const isTextTabActive = elements.textInputPane.classList.contains('show');

    if (isTextTabActive) {
        documentContent = elements.documentInput.value.trim();
        if (documentContent.length < 100) {
            showAlert('error', '문서 내용이 너무 짧습니다. (최소 100자)');
            return;
        }
    } else { // 파일 업로드 탭이 활성화된 경우
        documentContent = uploadedText;
        if (!documentContent || documentContent.length < 100) {
            showAlert('error', '업로드된 파일에서 추출된 텍스트가 너무 짧습니다. (최소 100자)');
            return;
        }
    }

    // 상태 저장 (여기서는 임시로 전역 변수에 저장)
    // 실제 애플리케이션에서는 `state` 객체 등을 사용할 수 있습니다.
    window.appState = window.appState || {};
    window.appState.document = documentContent;
    
    // UI 전환
    goToStep(2);
}

/**
 * PPT 생성 시작
 */
async function startGeneration() {
    try {
        // 로딩 표시
        elements.generatePPT.disabled = true;
        elements.generatePPT.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 생성 중...';

        // Step 3으로 이동
        goToStep(3);

        // 요청 데이터 준비
        const requestData = {
            document: window.appState.document, // 저장된 문서 내용 사용
            style: elements.styleSelect.value,
            target_audience: elements.audienceSelect.value,
            num_slides: parseInt(elements.numSlidesRange.value),
            language: elements.languageSelect.value
        };

        console.log('PPT 생성 요청:', requestData);
        const usePhasedMode = true; // 단계별 모드 활성화
        if (usePhasedMode) {
            await runPhasedFlow(requestData);
        } else {
            const response = await api.generatePPT(requestData);
            currentPPTId = response.ppt_id;
            console.log('PPT ID:', currentPPTId);
            startPolling();
        }

    } catch (error) {
        console.error('PPT 생성 실패:', error);
        showAlert('PPT 생성 중 오류가 발생했습니다: ' + error.message, 'danger');
        
        // 버튼 복원
        elements.generatePPT.disabled = false;
        elements.generatePPT.innerHTML = '<i class="fas fa-magic"></i> PPT 생성하기';
    }
}

// 간단한 GUID 생성기 (프로젝트 ID용)
function guid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

async function runPhasedFlow(req) {
    try {
        currentProjectId = guid();
        // 1) Analyze
        updateProgress(5); elements.currentStage.textContent = '분석(Phase 1)';
        await api.analyze({ project_id: currentProjectId, document: req.document, language: req.language });
        // 2) Structure
        updateProgress(20); elements.currentStage.textContent = '구조설계(Phase 2)';
        await api.structure({ project_id: currentProjectId, document: req.document, num_slides: req.num_slides, language: req.language });
        // 3) Content
        updateProgress(40); elements.currentStage.textContent = '콘텐츠생성(Phase 3)';
        await api.content({ project_id: currentProjectId, document: req.document, num_slides: req.num_slides, language: req.language });
        // 4) Design
        updateProgress(60); elements.currentStage.textContent = '디자인(Phase 4)';
        await api.design({ project_id: currentProjectId });
        // 5) Review
        updateProgress(80); elements.currentStage.textContent = '리뷰(Phase 5)';
        await api.review({ project_id: currentProjectId });
        // Export
        updateProgress(90); elements.currentStage.textContent = '내보내기';
        const exp = await api.export({ project_id: currentProjectId, document: req.document, num_slides: req.num_slides, language: req.language });
        if (exp && exp.result && exp.result.pptx_path) {
            updateProgress(100);
            elements.currentStage.textContent = '완료';
            elements.qualityScore.classList.remove('d-none');
            elements.scoreValue.textContent = (exp.result.quality_score || 0).toFixed(3);
            // phased 모드에서도 다운로드 버튼 활성화
            currentPPTId = currentProjectId;
        } else {
            showAlert('내보내기 실패: PPT 파일을 생성하지 못했습니다', 'danger');
        }
    } catch (e) {
        console.error('단계별 실행 실패:', e);
        showAlert('단계별 실행 중 오류가 발생했습니다: ' + (e.message || e), 'danger');
        elements.generatePPT.disabled = false;
        elements.generatePPT.innerHTML = '<i class="fas fa-magic"></i> PPT 생성하기';
    }
}

/**
 * 진행 상황 폴링 시작
 */
function startPolling() {
    // 즉시 한 번 실행
    pollStatus();

    // 1초마다 상태 확인
    pollInterval = setInterval(pollStatus, 1000);
}

/**
 * 상태 폴링
 */
async function pollStatus() {
    try {
        const status = await api.getPPTStatus(currentPPTId);
        
        console.log('현재 상태:', status);

        // 진행률 업데이트
        updateProgress(status.progress);

        // 현재 단계 업데이트
        if (status.current_stage) {
            updateCurrentStage(status.current_stage);
        }

        // 완료 처리
        if (status.status === 'completed') {
            clearInterval(pollInterval);
            handleCompletion(status);
        }

        // 실패 처리
        if (status.status === 'failed') {
            clearInterval(pollInterval);
            handleFailure(status);
        }

    } catch (error) {
        console.error('상태 조회 실패:', error);
    }
}

/**
 * 진행률 업데이트
 */
function updateProgress(progress) {
    elements.progressBar.style.width = `${progress}%`;
    elements.progressBar.textContent = `${progress}%`;
}

/**
 * 현재 단계 업데이트
 */
function updateCurrentStage(stage) {
    elements.currentStage.textContent = getStageName(stage);
    elements.stageDescription.textContent = stageDescriptions[stage] || '처리 중...';

    // 체크리스트 업데이트
    updateStageChecklist(stage);
}

/**
 * 단계 이름 가져오기
 */
function getStageName(stage) {
    const names = {
        'document_analysis': '문서 분석',
        'structure_design': '구조 설계',
        'content_generation': '콘텐츠 생성',
        'design_application': '디자인 적용',
        'quality_review': '품질 검토'
    };
    return names[stage] || stage;
}

/**
 * 단계 체크리스트 업데이트
 */
function updateStageChecklist(currentStage) {
    const stages = ['document_analysis', 'structure_design', 'content_generation', 'design_application', 'quality_review'];
    const currentIndex = stages.indexOf(currentStage);

    stages.forEach((stage, index) => {
        const item = document.querySelector(`.stage-item[data-stage="${stage}"]`);
        const icon = item.querySelector('i');

        if (index < currentIndex) {
            // 완료된 단계
            item.classList.remove('processing');
            item.classList.add('completed');
            icon.className = 'fas fa-check-circle';
        } else if (index === currentIndex) {
            // 현재 진행 중인 단계
            item.classList.add('processing');
            item.classList.remove('completed');
            icon.className = 'fas fa-circle-notch fa-spin';
        } else {
            // 대기 중인 단계
            item.classList.remove('processing', 'completed');
            icon.className = 'far fa-circle';
        }
    });
}

/**
 * 생성 완료 처리
 */
function handleCompletion(status) {
    console.log('PPT 생성 완료!', status);

    // 진행률 100%
    updateProgress(100);

    // 모든 단계 완료 표시
    document.querySelectorAll('.stage-item').forEach(item => {
        item.classList.add('completed');
        item.classList.remove('processing');
        item.querySelector('i').className = 'fas fa-check-circle';
    });

    // 품질 점수 표시
    elements.qualityScore.style.display = 'block';
    elements.scoreValue.textContent = (status.quality_score || 0).toFixed(3);
    
    // 생성 시간 계산
    const createdAt = new Date(status.created_at);
    const completedAt = new Date(status.completed_at);
    const duration = ((completedAt - createdAt) / 1000).toFixed(1);
    elements.generationTime.textContent = duration;

    // 다운로드 버튼 표시
    elements.downloadPPT.style.display = 'inline-block';
    elements.createNew.style.display = 'inline-block';

    // 성공 알림
    showAlert('PPT 생성이 완료되었습니다!', 'success');
}

/**
 * 생성 실패 처리
 */
function handleFailure(status) {
    console.error('PPT 생성 실패:', status);
    showAlert('PPT 생성 중 오류가 발생했습니다: ' + (status.error || '알 수 없는 오류'), 'danger');
    
    // 새로 만들기 버튼만 표시
    elements.createNew.style.display = 'inline-block';
}

/**
 * PPT 파일 다운로드
 */
function downloadPPTFile() {
    const downloadURL = api.getDownloadURL(currentPPTId);
    window.open(downloadURL, '_blank');
    
    showAlert('PPT 파일을 다운로드합니다...', 'info');
}

/**
 * 알림 표시
 */
function showAlert(message, type = 'info') {
    // 기존 알림 제거
    const existingAlerts = document.querySelectorAll('.alert-floating');
    existingAlerts.forEach(alert => alert.remove());

    // 새 알림 생성
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-floating`;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    `;
    alert.innerHTML = `
        <strong>${getAlertIcon(type)}</strong> ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;

    document.body.appendChild(alert);

    // 3초 후 자동 제거
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

/**
 * 알림 아이콘
 */
function getAlertIcon(type) {
    const icons = {
        'success': '<i class="fas fa-check-circle"></i>',
        'danger': '<i class="fas fa-exclamation-circle"></i>',
        'warning': '<i class="fas fa-exclamation-triangle"></i>',
        'info': '<i class="fas fa-info-circle"></i>'
    };
    return icons[type] || icons.info;
}

// ==========================================
// 파일 업로드 초기화
// ==========================================
function initFileUpload() {
    // 파일 선택 버튼 클릭
    elements.selectFileBtn.addEventListener('click', () => {
        elements.fileInput.click();
    });

    // 업로드 영역 클릭
    elements.uploadArea.addEventListener('click', (e) => {
        if (e.target === elements.uploadArea || e.target.closest('.upload-icon, .upload-area h3')) {
            elements.fileInput.click();
        }
    });

    // 파일 선택
    elements.fileInput.addEventListener('change', handleFileSelect);

    // 드래그 앤 드롭
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);

    // 파일 제거
    elements.removeFileBtn.addEventListener('click', clearUploadedFile);
}

// ==========================================
// 드래그 오버
// ==========================================
function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.add('drag-over');
}

// ==========================================
// 드래그 벗어남
// ==========================================
function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.remove('drag-over');
}

// ==========================================
// 드롭
// ==========================================
function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    elements.uploadArea.classList.remove('drag-over');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// ==========================================
// 파일 선택 핸들러
// ==========================================
function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

// ==========================================
// 파일 처리
// ==========================================
async function handleFile(file) {
    // 파일 형식 검증
    const allowedExtensions = ['.docx', '.pdf', '.md'];
    const fileName = file.name.toLowerCase();
    const hasValidExtension = allowedExtensions.some(ext => fileName.endsWith(ext));

    if (!hasValidExtension) {
        showAlert('error', '지원하지 않는 파일 형식입니다. (DOCX, PDF, MD만 가능)');
        return;
    }

    // 파일 크기 검증 (10MB)
    const maxSize = 10 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('error', `파일 크기가 너무 큽니다. (최대 10MB, 현재: ${(file.size / 1024 / 1024).toFixed(2)}MB)`);
        return;
    }

    // UI 업데이트 - 업로드 중
    showUploadProgress();

    try {
        // FormData 생성
        const formData = new FormData();
        formData.append('file', file);

        // API 호출
        const response = await fetch(`${API_BASE_URL}/api/v1/upload-document`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '파일 업로드 실패');
        }

        const result = await response.json();

        // 업로드 성공
        currentFile = {
            name: result.filename,
            size: result.file_size,
            format: result.format,
            text: result.text
        };

        uploadedText = result.text;

        // UI 업데이트 - 파일 정보 표시
        showFileInfo(currentFile);

        // 다음 버튼 활성화
        updateNextButton();

        showAlert('success', '파일이 성공적으로 업로드되었습니다!');

    } catch (error) {
        console.error('File upload error:', error);
        showAlert('error', `파일 업로드 실패: ${error.message}`);
        hideUploadProgress();
    }
}

// ==========================================
// 업로드 진행 상황 표시
// ==========================================
function showUploadProgress() {
    elements.uploadArea.style.display = 'none';
    elements.uploadProgress.style.display = 'block';
    elements.fileInfo.style.display = 'none';

    // 프로그레스 바 애니메이션
    elements.progressFill.style.width = '0%';

    setTimeout(() => {
        elements.progressFill.style.width = '90%';
    }, 100);
}

// ==========================================
// 업로드 진행 상황 숨기기
// ==========================================
function hideUploadProgress() {
    elements.uploadProgress.style.display = 'none';
    elements.uploadArea.style.display = 'block';
}

// ==========================================
// 파일 정보 표시
// ==========================================
function showFileInfo(file) {
    elements.uploadArea.style.display = 'none';
    elements.uploadProgress.style.display = 'none';
    elements.fileInfo.style.display = 'block';

    // 파일 이름
    elements.fileName.textContent = file.name;

    // 파일 크기
    const sizeInMB = (file.size / 1024 / 1024).toFixed(2);
    elements.fileSize.textContent = `${sizeInMB} MB · ${file.format.toUpperCase()} 문서`;

    // 미리보기 텍스트 (처음 500자)
    const previewLength = 500;
    const previewText = file.text.length > previewLength 
        ? file.text.substring(0, previewLength) + '...' 
        : file.text;
    elements.previewText.textContent = previewText;
}

// ==========================================
// 업로드된 파일 제거
// ==========================================
function clearUploadedFile() {
    currentFile = null;
    uploadedText = '';

    elements.fileInfo.style.display = 'none';
    elements.uploadArea.style.display = 'block';
    elements.fileInput.value = ''; // 파일 입력 초기화

    // 다음 버튼 비활성화
    updateNextButton();
}

// 디버깅용
window.debugAPI = api;
