// Study Planner - Main Application Logic
const API_BASE = 'http://127.0.0.1:8000';

// State Management
const state = {
    subjects: [],
    currentSubject: null,
    currentDocument: null,
    chunks: [],
    filteredChunks: []
};

// Utility Functions
function showLoading(text = 'Loading...') {
    const overlay = document.getElementById('loadingOverlay');
    const loadingText = document.getElementById('loadingText');
    loadingText.textContent = text;
    overlay.style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

// Navigation
function switchView(viewId) {
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(viewId).classList.add('active');
    
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector(`[data-view="${viewId.replace('View', '')}"]`)?.classList.add('active');
}

// API Functions
async function fetchSubjects() {
    try {
        showLoading('Loading subjects...');
        const response = await fetch(`${API_BASE}/api/subjects`);
        const data = await response.json();
        state.subjects = data.subjects || [];
        renderSubjects();
    } catch (error) {
        showToast('Failed to load subjects', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function createSubject(formData) {
    try {
        showLoading('Creating subject...');
        const response = await fetch(`${API_BASE}/api/subjects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) throw new Error('Failed to create subject');
        
        const subject = await response.json();
        showToast('Subject created successfully!', 'success');
        closeModal('subjectModal');
        fetchSubjects();
    } catch (error) {
        showToast('Failed to create subject', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function uploadDocument(file, subjectId) {
    try {
        showLoading('Uploading document...');
        const formData = new FormData();
        formData.append('file', file);
        formData.append('subject_id', subjectId);
        
        const response = await fetch(`${API_BASE}/api/documents/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        const document = await response.json();
        showToast('Document uploaded successfully!', 'success');
        
        // Auto-process document
        processDocument(document.id);
        
        return document;
    } catch (error) {
        showToast(error.message, 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function processDocument(documentId) {
    try {
        showLoading('Processing document...');
        const response = await fetch(`${API_BASE}/api/documents/${documentId}/process`, {
            method: 'POST'
        });
        
        if (!response.ok) throw new Error('Processing failed');
        
        const result = await response.json();
        showToast(`${result.message}`, 'success');
        
        // Fetch documents for current subject
        if (state.currentSubject) {
            fetchDocuments(state.currentSubject.id);
        }
    } catch (error) {
        showToast('Processing failed', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function fetchDocuments(subjectId) {
    try {
        showLoading('Loading documents...');
        const response = await fetch(`${API_BASE}/api/documents?subject_id=${subjectId}`);
        const data = await response.json();
        renderDocuments(data.documents || []);
    } catch (error) {
        showToast('Failed to load documents', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function fetchChunks(documentId, contentType = 'all') {
    try {
        showLoading('Loading content...');
        let url = `${API_BASE}/api/documents/${documentId}/chunks?limit=100`;
        if (contentType !== 'all') {
            url += `&content_type=${contentType}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        state.chunks = data.chunks || [];
        state.filteredChunks = state.chunks;
        
        // Fetch stats
        fetchChunkStats(documentId);
        
        renderChunks();
    } catch (error) {
        showToast('Failed to load chunks', 'error');
        console.error(error);
    } finally {
        hideLoading();
    }
}

async function fetchChunkStats(documentId) {
    try {
        const response = await fetch(`${API_BASE}/api/documents/${documentId}/chunks/stats`);
        const stats = await response.json();
        renderStats(stats);
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Render Functions
function renderSubjects() {
    const grid = document.getElementById('subjectsGrid');
    const emptyState = document.getElementById('emptyState');
    
    if (state.subjects.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    grid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    grid.innerHTML = state.subjects.map(subject => `
        <div class="subject-card" onclick="viewSubject('${subject.id}')">
            <div class="subject-card-header">
                <div>
                    <h3 class="subject-title">${subject.name}</h3>
                    <p class="subject-code">${subject.code || 'No code'}</p>
                </div>
                <span class="subject-priority">P${subject.priority}</span>
            </div>
            <div class="subject-stats">
                <div class="stat">
                    <span class="stat-value">${subject.chapters_count || 0}</span>
                    <span class="stat-label">Chapters</span>
                </div>
                <div class="stat">
                    <span class="stat-value">${subject.topics_count || 0}</span>
                    <span class="stat-label">Topics</span>
                </div>
                <div class="stat">
                    <span class="stat-value">${subject.documents_count || 0}</span>
                    <span class="stat-label">Documents</span>
                </div>
            </div>
        </div>
    `).join('');
}

function renderDocuments(documents) {
    const list = document.getElementById('documentsList');
    
    if (documents.length === 0) {
        list.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No documents uploaded yet</p>';
        return;
    }
    
    list.innerHTML = documents.map(doc => `
        <div class="document-item">
            <div class="document-info">
                <div class="document-name">${doc.filename}</div>
                <div class="document-meta">
                    ${doc.file_type.toUpperCase()} • 
                    ${(doc.file_size / 1024 / 1024).toFixed(2)} MB • 
                    Status: ${doc.processing_status}
                    ${doc.page_count ? ` • ${doc.page_count} pages` : ''}
                </div>
            </div>
            <div class="document-actions">
                ${doc.processing_status === 'pending' ? 
                    `<button class="btn-primary" onclick="processDocument('${doc.id}')">Process</button>` :
                    doc.processing_status === 'completed' ?
                    `<button class="btn-primary" onclick="viewChunks('${doc.id}')">View Content</button>` :
                    ''
                }
            </div>
        </div>
    `).join('');
}

function renderChunks() {
    const list = document.getElementById('chunksList');
    
    if (state.filteredChunks.length === 0) {
        list.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 2rem;">No chunks found</p>';
        return;
    }
    
    list.innerHTML = state.filteredChunks.map(chunk => `
        <div class="chunk-item">
            <div class="chunk-header">
                <span class="chunk-type ${chunk.content_type}">${chunk.content_type}</span>
                <div class="chunk-meta">
                    ${chunk.page_number ? `Page ${chunk.page_number} • ` : ''}
                    Confidence: ${(chunk.confidence_score * 100).toFixed(0)}%
                </div>
            </div>
            <div class="chunk-text">${chunk.raw_text}</div>
        </div>
    `).join('');
}

function renderStats(stats) {
    const panel = document.getElementById('statsPanel');
    
    panel.innerHTML = `
        <div class="stat">
            <span class="stat-value">${stats.total_chunks}</span>
            <span class="stat-label">Total Chunks</span>
        </div>
        <div class="stat">
            <span class="stat-value">${(stats.avg_confidence * 100).toFixed(0)}%</span>
            <span class="stat-label">Avg Confidence</span>
        </div>
        ${Object.entries(stats.by_type).map(([type, count]) => `
            <div class="stat">
                <span class="stat-value">${count}</span>
                <span class="stat-label">${type}</span>
            </div>
        `).join('')}
    `;
}

// View Functions
function viewSubject(subjectId) {
    const subject = state.subjects.find(s => s.id === subjectId);
    if (!subject) return;
    
    state.currentSubject = subject;
    
    document.getElementById('subjectDetails').innerHTML = `
        <h3>${subject.name}</h3>
        <p style="color: var(--text-secondary); margin-bottom: 1rem;">${subject.code || 'No code'}</p>
    `;
    
    switchView('documentsView');
    fetchDocuments(subjectId);
}

function viewChunks(documentId) {
    state.currentDocument = documentId;
    switchView('analyticsView');
    fetchChunks(documentId);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Load subjects on startup
    fetchSubjects();
    
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', () => {
            const view = item.dataset.view + 'View';
            switchView(view);
        });
    });
    
    // New Subject Button
    document.getElementById('newSubjectBtn').addEventListener('click', () => {
        openModal('subjectModal');
    });
    
    // Subject Form
    document.getElementById('subjectForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = {
            name: e.target.name.value,
            code: e.target.code.value || null,
            exam_date: e.target.exam_date.value || null,
            priority: parseInt(e.target.priority.value)
        };
        await createSubject(formData);
        e.target.reset();
    });
    
    // File Upload
    const fileInput = document.getElementById('fileInput');
    const uploadBox = document.querySelector('.upload-box');
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0 && state.currentSubject) {
            uploadDocument(e.target.files[0], state.currentSubject.id);
        }
    });
    
    // Drag & Drop
    uploadBox.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadBox.classList.add('drag-over');
    });
    
    uploadBox.addEventListener('dragleave', () => {
        uploadBox.classList.remove('drag-over');
    });
    
    uploadBox.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadBox.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0 && state.currentSubject) {
            uploadDocument(e.dataTransfer.files[0], state.currentSubject.id);
        }
    });
    
    // Back Buttons
    document.getElementById('backToSubjects').addEventListener('click', () => {
        switchView('dashboardView');
    });
    
    document.getElementById('backToDocuments').addEventListener('click', () => {
        switchView('documentsView');
    });
    
    // Filter Buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const type = btn.dataset.type;
            if (type === 'all') {
                state.filteredChunks = state.chunks;
            } else {
                state.filteredChunks = state.chunks.filter(c => c.content_type === type);
            }
            renderChunks();
        });
    });
});

// Make functions globally available
window.closeModal = closeModal;
window.viewSubject = viewSubject;
window.viewChunks = viewChunks;
window.processDocument = processDocument;
