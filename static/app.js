/**
 * PaddleOCR-VL-1.6 Stock Count AI Studio • Frontend Client Controller
 */

// Application Global State
const state = {
  currentScan: null, // Full API response
  activePageIndex: 0,
  activeFilter: 'ALL', // ALL | DISCREPANCY | MATCHED
  searchTerm: '',
  theme: localStorage.getItem('ocr_theme') || 'dark',
  
  // Canvas Transform State
  scale: 1.0,
  panX: 0,
  panY: 0,
  rotation: 0,
  isPanning: false,
  startX: 0,
  startY: 0,

  // Layers Visibility
  showBoxes: true,
  showLabels: true,
  showDiscrepancy: true,

  // Samples Cache
  samples: []
};

// DOM Element Selectors
const elements = {
  appContainer: document.getElementById('app-container'),
  btnTheme: document.getElementById('btn-theme'),
  themeMoon: document.getElementById('theme-icon-moon'),
  themeSun: document.getElementById('theme-icon-sun'),
  
  // Header Actions
  btnSamples: document.getElementById('btn-samples'),
  fileInput: document.getElementById('file-upload-input'),
  btnExportDropdown: document.getElementById('btn-export-dropdown'),
  exportMenu: document.getElementById('export-menu'),
  
  // Export Actions
  exportExcelBtn: document.getElementById('export-excel-btn'),
  exportCsvBtn: document.getElementById('export-csv-btn'),
  exportJsonBtn: document.getElementById('export-json-btn'),
  exportMdBtn: document.getElementById('export-md-btn'),

  // Canvas
  canvasViewport: document.getElementById('canvas-viewport'),
  canvasDropzone: document.getElementById('canvas-dropzone'),
  canvasStage: document.getElementById('canvas-stage'),
  canvasTransform: document.getElementById('canvas-transform'),
  docImage: document.getElementById('doc-image'),
  overlaySvg: document.getElementById('overlay-svg'),
  loadingOverlay: document.getElementById('loading-overlay'),
  zoomText: document.getElementById('zoom-level-text'),
  
  // Canvas Tools
  btnZoomIn: document.getElementById('btn-zoom-in'),
  btnZoomOut: document.getElementById('btn-zoom-out'),
  btnFitScreen: document.getElementById('btn-fit-screen'),
  btnRotate: document.getElementById('btn-rotate'),
  btnResetView: document.getElementById('btn-reset-view'),
  
  // Layer Toggles
  toggleBoxes: document.getElementById('toggle-boxes'),
  toggleLabels: document.getElementById('toggle-labels'),
  toggleDiscrepancy: document.getElementById('toggle-discrepancy'),

  // Metadata Card
  metaDocNo: document.getElementById('meta-doc-no'),
  metaWarehouse: document.getElementById('meta-warehouse'),
  metaDate: document.getElementById('meta-date'),
  metaAuditor: document.getElementById('meta-auditor'),
  metaLatency: document.getElementById('meta-latency'),
  metaStatusText: document.getElementById('meta-status-text'),

  // KPIs
  kpiTotalSkus: document.getElementById('kpi-total-skus'),
  kpiMatchRate: document.getElementById('kpi-match-rate'),
  kpiMatchedSkus: document.getElementById('kpi-matched-skus'),
  kpiSurplusUnits: document.getElementById('kpi-surplus-units'),
  kpiDeficitUnits: document.getElementById('kpi-deficit-units'),
  tabCountBadge: document.getElementById('tab-count-badge'),

  // Table & Tabs
  tabButtons: document.querySelectorAll('.tab-btn'),
  tabContents: document.querySelectorAll('.tab-content'),
  tableSearch: document.getElementById('table-search'),
  filterPills: document.querySelectorAll('.filter-pill'),
  stockTableBody: document.getElementById('stock-table-body'),
  btnAddRow: document.getElementById('btn-add-row'),
  
  markdownCodeView: document.getElementById('markdown-code-view'),
  jsonCodeView: document.getElementById('json-code-view'),
  blocksTableBody: document.getElementById('blocks-table-body'),
  
  btnCopyMd: document.getElementById('btn-copy-md'),
  btnCopyJson: document.getElementById('btn-copy-json'),

  // Modal
  samplesModal: document.getElementById('samples-modal'),
  btnCloseModal: document.getElementById('btn-close-modal'),
  samplesListContainer: document.getElementById('samples-list-container'),
  btnQuickSampleStart: document.getElementById('btn-quick-sample-start'),
  toastContainer: document.getElementById('toast-container')
};

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initEventListeners();
  initCanvasInteraction();
  loadSamplesList();
});

/* ==========================================================================
   Theme Management
   ========================================================================== */
function initTheme() {
  document.documentElement.setAttribute('data-theme', state.theme);
  updateThemeIcons();
}

function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  localStorage.setItem('ocr_theme', state.theme);
  document.documentElement.setAttribute('data-theme', state.theme);
  updateThemeIcons();
}

function updateThemeIcons() {
  if (state.theme === 'dark') {
    elements.themeMoon.classList.remove('hidden');
    elements.themeSun.classList.add('hidden');
  } else {
    elements.themeMoon.classList.add('hidden');
    elements.themeSun.classList.remove('hidden');
  }
}

/* ==========================================================================
   Event Listeners Setup
   ========================================================================== */
function initEventListeners() {
  // Theme Toggle
  elements.btnTheme.addEventListener('click', toggleTheme);

  // Upload File
  elements.fileInput.addEventListener('change', handleFileUpload);

  // Export Menu Toggle
  elements.btnExportDropdown.addEventListener('click', (e) => {
    e.stopPropagation();
    elements.btnExportDropdown.parentElement.classList.toggle('open');
  });

  document.addEventListener('click', () => {
    elements.btnExportDropdown.parentElement.classList.remove('open');
  });

  // Export Actions
  elements.exportExcelBtn.addEventListener('click', (e) => { e.preventDefault(); exportData('excel'); });
  elements.exportCsvBtn.addEventListener('click', (e) => { e.preventDefault(); exportData('csv'); });
  elements.exportJsonBtn.addEventListener('click', (e) => { e.preventDefault(); exportData('json'); });
  elements.exportMdBtn.addEventListener('click', (e) => { e.preventDefault(); exportData('markdown'); });

  // Tab Navigation
  elements.tabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      elements.tabButtons.forEach(b => b.classList.remove('active'));
      elements.tabContents.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });

  // Filter Pills
  elements.filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      elements.filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      state.activeFilter = pill.getAttribute('data-filter');
      renderStockTable();
    });
  });

  // Search input
  elements.tableSearch.addEventListener('input', (e) => {
    state.searchTerm = e.target.value.toLowerCase();
    renderStockTable();
  });

  // Add Row
  elements.btnAddRow.addEventListener('click', addNewStockRow);

  // Copy Buttons
  elements.btnCopyMd.addEventListener('click', () => {
    navigator.clipboard.writeText(elements.markdownCodeView.textContent);
    showToast('Đã copy nội dung Markdown!', 'success');
  });

  elements.btnCopyJson.addEventListener('click', () => {
    navigator.clipboard.writeText(elements.jsonCodeView.textContent);
    showToast('Đã copy cấu trúc JSON!', 'success');
  });

  // Samples Modal
  elements.btnSamples.addEventListener('click', openSamplesModal);
  elements.btnQuickSampleStart.addEventListener('click', openSamplesModal);
  elements.btnCloseModal.addEventListener('click', closeSamplesModal);
  elements.samplesModal.addEventListener('click', (e) => {
    if (e.target === elements.samplesModal) closeSamplesModal();
  });

  // Layer Toggles
  elements.toggleBoxes.addEventListener('change', (e) => {
    state.showBoxes = e.target.checked;
    updateSvgLayerVisibility();
  });
  elements.toggleLabels.addEventListener('change', (e) => {
    state.showLabels = e.target.checked;
    updateSvgLayerVisibility();
  });
  elements.toggleDiscrepancy.addEventListener('change', (e) => {
    state.showDiscrepancy = e.target.checked;
    updateSvgLayerVisibility();
  });

  // Drag and Drop on Canvas
  const dropzone = elements.canvasViewport;
  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      elements.canvasDropzone.querySelector('.dropzone-card')?.classList.add('drag-over');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, (e) => {
      e.preventDefault();
      elements.canvasDropzone.querySelector('.dropzone-card')?.classList.remove('drag-over');
    }, false);
  });

  dropzone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      scanDocumentFile(files[0]);
    }
  });
}

/* ==========================================================================
   Canvas Pan / Zoom & Visual Interaction
   ========================================================================== */
function initCanvasInteraction() {
  elements.btnZoomIn.addEventListener('click', () => zoomCanvas(1.2));
  elements.btnZoomOut.addEventListener('click', () => zoomCanvas(1 / 1.2));
  elements.btnFitScreen.addEventListener('click', fitCanvasToScreen);
  elements.btnRotate.addEventListener('click', () => {
    state.rotation = (state.rotation + 90) % 360;
    applyCanvasTransform();
  });
  elements.btnResetView.addEventListener('click', resetCanvasTransform);

  // Wheel Zoom
  elements.canvasViewport.addEventListener('wheel', (e) => {
    if (!state.currentScan) return;
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 1 / 1.15;
    zoomCanvas(zoomFactor);
  });

  // Mouse Drag Panning
  elements.canvasViewport.addEventListener('mousedown', (e) => {
    if (e.target.tagName.toLowerCase() === 'rect' || e.target.tagName.toLowerCase() === 'text') return;
    state.isPanning = true;
    elements.canvasViewport.classList.add('panning');
    state.startX = e.clientX - state.panX;
    state.startY = e.clientY - state.panY;
  });

  window.addEventListener('mousemove', (e) => {
    if (!state.isPanning) return;
    state.panX = e.clientX - state.startX;
    state.panY = e.clientY - state.startY;
    applyCanvasTransform();
  });

  window.addEventListener('mouseup', () => {
    state.isPanning = false;
    elements.canvasViewport.classList.remove('panning');
  });
}

function zoomCanvas(factor) {
  state.scale = Math.min(Math.max(state.scale * factor, 0.2), 5.0);
  elements.zoomText.textContent = `${Math.round(state.scale * 100)}%`;
  applyCanvasTransform();
}

function fitCanvasToScreen() {
  if (!elements.docImage.naturalWidth) return;
  const viewportW = elements.canvasViewport.clientWidth - 40;
  const viewportH = elements.canvasViewport.clientHeight - 40;
  const imgW = elements.docImage.naturalWidth;
  const imgH = elements.docImage.naturalHeight;

  const scaleW = viewportW / imgW;
  const scaleH = viewportH / imgH;
  state.scale = Math.min(scaleW, scaleH, 1.0);
  
  // Center
  state.panX = (elements.canvasViewport.clientWidth - imgW * state.scale) / 2;
  state.panY = (elements.canvasViewport.clientHeight - imgH * state.scale) / 2;
  state.rotation = 0;

  elements.zoomText.textContent = `${Math.round(state.scale * 100)}%`;
  applyCanvasTransform();
}

function resetCanvasTransform() {
  state.scale = 1.0;
  state.panX = 0;
  state.panY = 0;
  state.rotation = 0;
  elements.zoomText.textContent = '100%';
  applyCanvasTransform();
}

function applyCanvasTransform() {
  elements.canvasStage.style.transform = `translate(${state.panX}px, ${state.panY}px) scale(${state.scale}) rotate(${state.rotation}deg)`;
}

/* ==========================================================================
   OCR Scanning & Data Handling
   ========================================================================== */
function handleFileUpload(e) {
  const file = e.target.files[0];
  if (file) {
    scanDocumentFile(file);
  }
}

async function scanDocumentFile(file) {
  const formData = new FormData();
  formData.append('file', file);
  await executeScanApi(formData);
}

async function scanSampleDocument(sampleId) {
  closeSamplesModal();
  const formData = new FormData();
  formData.append('sample_id', sampleId);
  await executeScanApi(formData);
}

async function executeScanApi(formData) {
  setLoading(true);
  try {
    const response = await fetch('/api/scan', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.detail || 'Lỗi xử lý OCR tài liệu');
    }

    const data = await response.json();
    state.currentScan = data;
    state.activePageIndex = 0;

    // Render Data into All Panels
    renderScannedResults();
    elements.btnExportDropdown.disabled = false;
    showToast(`Quét thành công! PaddleOCR-VL-1.6 xử lý trong ${data.total_execution_time_ms} ms`, 'success');

  } catch (error) {
    console.error('Scan error:', error);
    showToast(`Lỗi quét tài liệu: ${error.message}`, 'error');
  } finally {
    setLoading(false);
  }
}

function setLoading(isLoading) {
  if (isLoading) {
    elements.loadingOverlay.classList.remove('hidden');
  } else {
    elements.loadingOverlay.classList.add('hidden');
  }
}

/* ==========================================================================
   Results Rendering (Canvas, Metadata, KPIs, Table, Code)
   ========================================================================== */
function renderScannedResults() {
  if (!state.currentScan || !state.currentScan.pages || state.currentScan.pages.length === 0) return;

  const page = state.currentScan.pages[state.activePageIndex];
  
  // 1. Hide Dropzone and Show Canvas Stage
  elements.canvasDropzone.style.display = 'none';
  elements.canvasStage.classList.add('active');

  // 2. Set Image Source
  elements.docImage.src = page.image_data;
  elements.docImage.onload = () => {
    fitCanvasToScreen();
    renderSvgOverlay(page);
  };

  // 3. Render Metadata Block
  const meta = state.currentScan.metadata || {};
  elements.metaDocNo.textContent = meta.document_no || 'Phiếu Kiểm Kê';
  elements.metaWarehouse.textContent = meta.warehouse || '-';
  elements.metaDate.textContent = meta.count_date || '-';
  elements.metaAuditor.textContent = meta.auditor || '-';
  elements.metaLatency.textContent = `${state.currentScan.total_execution_time_ms} ms`;
  elements.metaStatusText.textContent = `${state.currentScan.model_used || 'PaddleOCR-VL-1.6'}`;

  // 4. Update KPIs
  updateKpiDisplay(state.currentScan.kpi);

  // 5. Render Stock Count Table
  renderStockTable();

  // 6. Render Markdown View
  elements.markdownCodeView.textContent = state.currentScan.markdown || 'Không có Markdown';

  // 7. Render JSON View
  elements.jsonCodeView.textContent = JSON.stringify(state.currentScan, null, 2);

  // 8. Render Layout Blocks Table
  renderBlocksTable(page.blocks || []);
}

function updateKpiDisplay(kpi) {
  if (!kpi) return;
  elements.kpiTotalSkus.textContent = kpi.total_skus || 0;
  elements.kpiMatchRate.textContent = `${kpi.match_rate_pct || 0}%`;
  elements.kpiMatchedSkus.textContent = `${kpi.matched_skus || 0}`;
  elements.kpiSurplusUnits.textContent = `+${kpi.surplus_units || 0}`;
  elements.kpiDeficitUnits.textContent = `-${kpi.deficit_units || 0}`;
  elements.tabCountBadge.textContent = kpi.total_skus || 0;
}

/* ==========================================================================
   SVG Bounding Box Overlay & Hover Sync
   ========================================================================== */
function renderSvgOverlay(page) {
  const svg = elements.overlaySvg;
  svg.innerHTML = '';
  svg.setAttribute('viewBox', `0 0 ${page.width} ${page.height}`);
  svg.setAttribute('width', page.width);
  svg.setAttribute('height', page.height);

  const items = state.currentScan.items || [];
  
  items.forEach((item) => {
    if (!item.bbox || item.bbox.length < 4) return;
    const [x1, y1, x2, y2] = item.bbox;
    const w = x2 - x1;
    const h = y2 - y1;

    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x1);
    rect.setAttribute('y', y1);
    rect.setAttribute('width', w);
    rect.setAttribute('height', h);
    rect.setAttribute('rx', 4);
    rect.setAttribute('id', `svg-box-${item.id}`);

    let boxClass = 'ocr-box';
    if (item.status === 'MATCHED') boxClass += ' box-matched';
    else boxClass += ' box-discrepancy';
    rect.setAttribute('class', boxClass);

    // Hover & Click Sync with table row
    rect.addEventListener('mouseenter', () => highlightRowAndBox(item.id, true));
    rect.addEventListener('mouseleave', () => highlightRowAndBox(item.id, false));
    rect.addEventListener('click', () => {
      const row = document.getElementById(`row-item-${item.id}`);
      row?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      highlightRowAndBox(item.id, true);
    });

    svg.appendChild(rect);
  });
}

function updateSvgLayerVisibility() {
  const svg = elements.overlaySvg;
  svg.style.display = state.showBoxes ? 'block' : 'none';
  
  const discrepancyBoxes = svg.querySelectorAll('.box-discrepancy');
  discrepancyBoxes.forEach(b => {
    b.style.display = state.showDiscrepancy ? 'block' : 'none';
  });
}

function highlightRowAndBox(itemId, isHighlight) {
  const row = document.getElementById(`row-item-${itemId}`);
  const box = document.getElementById(`svg-box-${itemId}`);

  if (isHighlight) {
    row?.classList.add('row-selected');
    box?.classList.add('highlighted');
  } else {
    row?.classList.remove('row-selected');
    box?.classList.remove('highlighted');
  }
}

/* ==========================================================================
   Stock Count Table Rendering & Inline Editing
   ========================================================================== */
function renderStockTable() {
  const tbody = elements.stockTableBody;
  tbody.innerHTML = '';

  const items = state.currentScan?.items || [];
  
  // Filter and Search
  const filtered = items.filter(item => {
    // Status Filter
    if (state.activeFilter === 'DISCREPANCY' && item.status === 'MATCHED') return false;
    if (state.activeFilter === 'MATCHED' && item.status !== 'MATCHED') return false;

    // Search Filter
    if (state.searchTerm) {
      const targetStr = `${item.sku} ${item.description} ${item.location} ${item.lot_batch} ${item.remarks}`.toLowerCase();
      if (!targetStr.includes(state.searchTerm)) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="13" class="text-center">Không tìm thấy mục kiểm kê nào phù hợp với bộ lọc.</td></tr>`;
    return;
  }

  filtered.forEach((item, index) => {
    const tr = document.createElement('tr');
    tr.id = `row-item-${item.id}`;

    let statusPillClass = 'status-pill matched';
    if (item.status === 'SURPLUS') statusPillClass = 'status-pill surplus';
    if (item.status === 'DEFICIT') statusPillClass = 'status-pill deficit';

    tr.innerHTML = `
      <td class="text-center text-muted font-mono">${item.stt || (index + 1)}</td>
      <td class="editable-cell font-mono" contenteditable="true" data-field="sku">${escapeHtml(item.sku)}</td>
      <td class="editable-cell" contenteditable="true" data-field="description">${escapeHtml(item.description)}</td>
      <td class="editable-cell text-center" contenteditable="true" data-field="uom">${escapeHtml(item.uom)}</td>
      <td class="editable-cell text-center font-mono" contenteditable="true" data-field="location">${escapeHtml(item.location || '')}</td>
      <td class="editable-cell text-right font-mono" contenteditable="true" data-field="book_qty">${item.book_qty}</td>
      <td class="editable-cell text-right font-mono font-bold" contenteditable="true" data-field="actual_qty">${item.actual_qty}</td>
      <td class="text-right font-mono font-bold ${item.variance < 0 ? 'text-rose' : (item.variance > 0 ? 'text-amber' : 'text-emerald')}">${item.variance > 0 ? '+' : ''}${item.variance}</td>
      <td class="text-center"><span class="${statusPillClass}">${item.status_text}</span></td>
      <td class="editable-cell text-center font-mono" contenteditable="true" data-field="lot_batch">${escapeHtml(item.lot_batch || '')}</td>
      <td class="editable-cell text-center font-mono" contenteditable="true" data-field="expiry">${escapeHtml(item.expiry || '')}</td>
      <td class="editable-cell" contenteditable="true" data-field="remarks">${escapeHtml(item.remarks || '')}</td>
      <td class="text-center">
        <button class="btn-delete-row" title="Xóa dòng" data-id="${item.id}">✕</button>
      </td>
    `;

    // Row hover sync with canvas
    tr.addEventListener('mouseenter', () => highlightRowAndBox(item.id, true));
    tr.addEventListener('mouseleave', () => highlightRowAndBox(item.id, false));

    // Handle Inline Edit on Blur
    tr.querySelectorAll('.editable-cell').forEach(cell => {
      cell.addEventListener('blur', () => handleCellEdit(item.id, cell.getAttribute('data-field'), cell.textContent.trim()));
      cell.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          cell.blur();
        }
      });
    });

    // Handle Delete Row
    tr.querySelector('.btn-delete-row')?.addEventListener('click', (e) => {
      e.stopPropagation();
      deleteStockRow(item.id);
    });

    tbody.appendChild(tr);
  });
}

function handleCellEdit(itemId, field, newValue) {
  const item = state.currentScan?.items.find(i => i.id === itemId);
  if (!item) return;

  if (field === 'book_qty' || field === 'actual_qty') {
    const numVal = parseFloat(newValue.replace(/,/g, '')) || 0;
    item[field] = numVal;

    // Recalculate Variance & Status
    item.variance = Math.round((item.actual_qty - item.book_qty) * 100) / 100;
    if (Math.abs(item.variance) < 1e-4) {
      item.status = 'MATCHED';
      item.status_text = 'Khớp (Matched)';
      item.status_color = '#10b981';
    } else if (item.variance > 0) {
      item.status = 'SURPLUS';
      item.status_text = `Thừa +${item.variance}`;
      item.status_color = '#f59e0b';
    } else {
      item.status = 'DEFICIT';
      item.status_text = `Thiếu ${item.variance}`;
      item.status_color = '#ef4444';
    }
  } else {
    item[field] = newValue;
  }

  // Recalculate Combined KPIs
  recalculateAllKpis();
  renderStockTable();
  elements.jsonCodeView.textContent = JSON.stringify(state.currentScan, null, 2);
}

function recalculateAllKpis() {
  const items = state.currentScan?.items || [];
  const total_skus = items.length;
  const total_book = items.reduce((sum, i) => sum + (Number(i.book_qty) || 0), 0);
  const total_actual = items.reduce((sum, i) => sum + (Number(i.actual_qty) || 0), 0);
  const matched_skus = items.filter(i => i.status === 'MATCHED').length;
  const discrepancy_skus = total_skus - matched_skus;
  const match_rate = total_skus > 0 ? Math.round((matched_skus / total_skus) * 1000) / 10 : 100;
  
  const surplus_units = items.filter(i => i.variance > 0).reduce((sum, i) => sum + i.variance, 0);
  const deficit_units = Math.abs(items.filter(i => i.variance < 0).reduce((sum, i) => sum + i.variance, 0));

  const kpi = {
    total_skus,
    total_book_qty: total_book,
    total_actual_qty: total_actual,
    matched_skus,
    discrepancy_skus,
    match_rate_pct: match_rate,
    surplus_units,
    deficit_units,
    net_variance_units: total_actual - total_book
  };

  state.currentScan.kpi = kpi;
  updateKpiDisplay(kpi);
}

function addNewStockRow() {
  if (!state.currentScan) return;
  const items = state.currentScan.items;
  const newId = items.length > 0 ? Math.max(...items.map(i => i.id)) + 1 : 1;

  const newItem = {
    id: newId,
    stt: items.length + 1,
    sku: `SKU-${String(newId).padStart(4, '0')}`,
    description: 'Sản phẩm mới thêm',
    uom: 'Cái',
    location: 'Kệ A1-01',
    book_qty: 10,
    actual_qty: 10,
    variance: 0,
    status: 'MATCHED',
    status_text: 'Khớp (Matched)',
    status_color: '#10b981',
    lot_batch: `LOT-${2026000 + newId}`,
    expiry: '2027-12-31',
    remarks: 'Nhập tay',
    bbox: [40, 200, 1160, 240]
  };

  items.push(newItem);
  recalculateAllKpis();
  renderStockTable();
  showToast('Đã thêm dòng mới vào bảng kiểm kê', 'info');
}

function deleteStockRow(itemId) {
  if (!state.currentScan) return;
  state.currentScan.items = state.currentScan.items.filter(i => i.id !== itemId);
  recalculateAllKpis();
  renderStockTable();
  showToast('Đã xóa dòng', 'info');
}

/* ==========================================================================
   OCR Layout Blocks Table Rendering
   ========================================================================== */
function renderBlocksTable(blocks) {
  const tbody = elements.blocksTableBody;
  tbody.innerHTML = '';

  if (!blocks || blocks.length === 0) {
    tbody.innerHTML = `<tr class="empty-row"><td colspan="5" class="text-center">Không có khối OCR.</td></tr>`;
    return;
  }

  blocks.forEach((b, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td class="text-center text-muted font-mono">${idx + 1}</td>
      <td><span class="badge-chip font-mono">${escapeHtml(b.label || 'text')}</span></td>
      <td class="font-mono text-muted">[${b.bbox ? b.bbox.join(', ') : '0,0,0,0'}]</td>
      <td class="font-mono text-emerald">${Math.round((b.score || 0.95) * 100)}%</td>
      <td>${escapeHtml(b.text || '')}</td>
    `;
    tbody.appendChild(tr);
  });
}

/* ==========================================================================
   Export Data Center
   ========================================================================== */
async function exportData(format) {
  if (!state.currentScan) return;

  const payload = {
    metadata: {
      warehouse: elements.metaWarehouse.textContent.trim(),
      document_no: elements.metaDocNo.textContent.trim(),
      count_date: elements.metaDate.textContent.trim(),
      auditor: elements.metaAuditor.textContent.trim(),
      count_type: 'Kiểm kê định kỳ (Periodic Cycle Count)'
    },
    items: state.currentScan.items,
    kpi: state.currentScan.kpi
  };

  try {
    const response = await fetch(`/api/export/${format}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) throw new Error('Export failed');

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    const docNo = payload.metadata.document_no.replace(/[^a-zA-Z0-9]/g, '_');
    const extMap = { excel: 'xlsx', csv: 'csv', json: 'json', markdown: 'md' };
    a.download = `StockCount_Audit_${docNo}.${extMap[format]}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    showToast(`Xuất file ${extMap[format].toUpperCase()} thành công!`, 'success');
  } catch (error) {
    showToast(`Lỗi xuất dữ liệu: ${error.message}`, 'error');
  }
}

/* ==========================================================================
   Samples Modal
   ========================================================================== */
async function loadSamplesList() {
  try {
    const res = await fetch('/api/samples');
    if (!res.ok) return;
    const data = await res.json();
    state.samples = data.samples || [];
    renderSamplesModal();
  } catch (e) {
    console.warn('Could not fetch samples:', e);
  }
}

function renderSamplesModal() {
  const container = elements.samplesListContainer;
  container.innerHTML = '';

  state.samples.forEach(sample => {
    const card = document.createElement('div');
    card.className = 'sample-card';
    card.innerHTML = `
      <div class="sample-thumb-box">
        <img src="${sample.image_url}" alt="${escapeHtml(sample.title)}">
        <span class="sample-badge">${sample.items_count} SKUs</span>
      </div>
      <div class="sample-info">
        <div class="sample-title">${escapeHtml(sample.title)}</div>
        <div class="sample-summary">${escapeHtml(sample.description)}</div>
        <div class="sample-footer">
          <span>${sample.category}</span>
          <span>Quét Ngay →</span>
        </div>
      </div>
    `;

    card.addEventListener('click', () => scanSampleDocument(sample.id));
    container.appendChild(card);
  });
}

function openSamplesModal() {
  elements.samplesModal.classList.remove('hidden');
}

function closeSamplesModal() {
  elements.samplesModal.classList.add('hidden');
}

/* ==========================================================================
   Toast Notification Utility
   ========================================================================== */
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const iconMap = {
    success: '✓',
    error: '✕',
    info: 'ℹ'
  };

  toast.innerHTML = `<span>${iconMap[type] || 'ℹ'}</span> <span>${escapeHtml(message)}</span>`;
  elements.toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.2s ease';
    setTimeout(() => toast.remove(), 200);
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
