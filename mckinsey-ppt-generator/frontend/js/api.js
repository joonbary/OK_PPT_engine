/**
 * API 통신 모듈
 * FastAPI 백엔드와 통신
 */

// 동일 출처 요청으로 CORS 회피 (Nginx가 /api/ 프록시)
const API_BASE_URL = '';

class APIClient {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    /**
     * PPT 생성 요청
     */
    async generatePPT(data) {
        try {
            const form = new FormData();
            if (data.document) form.append('document_text', data.document);
            if (data.num_slides) form.append('num_slides', String(data.num_slides));
            if (data.target_audience) form.append('target_audience', data.target_audience);
            if (data.style) form.append('style', data.style);
            if (data.language) form.append('language', data.language);

            const response = await fetch(`${this.baseURL}/api/v1/generate-ppt`, {
                method: 'POST',
                body: form,
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('PPT 생성 요청 실패:', error);
            throw error;
        }
    }

    /**
     * PPT 생성 상태 조회
     */
    async getPPTStatus(pptId) {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/ppt-status/${pptId}`);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('상태 조회 실패:', error);
            throw error;
        }
    }

    /**
     * PPT 파일 다운로드 URL 생성
     */
    getDownloadURL(pptId) {
        return `${this.baseURL}/api/v1/download/${pptId}`;
    }

    /**
     * PPT 삭제
     */
    async deletePPT(pptId) {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/ppt/${pptId}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('PPT 삭제 실패:', error);
            throw error;
        }
    }

    /**
     * 헬스 체크
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/api/v1/health`);
            return await response.json();
        } catch (error) {
            console.error('헬스 체크 실패:', error);
            return { status: 'error' };
        }
    }

    // Phased APIs
    async analyze(data) {
        const res = await fetch(`${this.baseURL}/api/v1/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: data.project_id,
                document: data.document,
                language: data.language || 'ko'
            })
        });
        return res.json();
    }
    async structure(data) {
        const res = await fetch(`${this.baseURL}/api/v1/structure`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: data.project_id,
                document: data.document,
                num_slides: data.num_slides || 10,
                language: data.language || 'ko'
            })
        });
        return res.json();
    }
    async content(data) {
        const res = await fetch(`${this.baseURL}/api/v1/content`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: data.project_id,
                document: data.document,
                num_slides: data.num_slides || 10,
                language: data.language || 'ko'
            })
        });
        return res.json();
    }
    async design(data) {
        const res = await fetch(`${this.baseURL}/api/v1/design`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: data.project_id })
        });
        return res.json();
    }
    async review(data) {
        const res = await fetch(`${this.baseURL}/api/v1/review`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_id: data.project_id })
        });
        return res.json();
    }
    async export(data) {
        const res = await fetch(`${this.baseURL}/api/v1/export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                project_id: data.project_id,
                document: data.document,
                num_slides: data.num_slides || 10,
                language: data.language || 'ko'
            })
        });
        return res.json();
    }
}

// API 클라이언트 인스턴스 생성
const api = new APIClient();
