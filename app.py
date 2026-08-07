import streamlit as st
import streamlit.components.v1 as components

# --- 1. CẤU HÌNH TRANG TỐI GIẢN & SIÊU NHẸ ---
st.set_page_config(
    page_title="In Ảnh Hàng Loạt - Smart Studio", 
    layout="wide", 
    page_icon="🖨️"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
    }
    
    .brand-container {
        text-align: center;
        padding: 15px 10px;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
    }
    .main-title {
        font-size: 1.6rem;
        color: #ffffff;
        font-weight: 800;
        margin: 0;
    }
    .sub-title {
        font-size: 0.85rem;
        color: #bfdbfe;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand-container">
    <div class="main-title">🖨️ HỆ THỐNG XẾP IN HỒ SƠ HÀNG LOẠT</div>
    <div class="sub-title">Công cụ tối ưu hóa trang in A4 cho hồ sơ 10 người - Siêu nhẹ & Siêu tốc</div>
</div>
""", unsafe_allow_html=True)

# --- 2. MODULE IN HÀNG LOẠT HTML/JS (CHẠY CLIENT-SIDE) ---
html_code = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: #ffffff; 
            display: flex; justify-content: center; align-items: flex-start; 
            margin: 0; padding: 10px 0;
        }
        .container { 
            background: #ffffff; padding: 20px 25px; border-radius: 16px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.06); max-width: 850px; width: 100%; text-align: center;
            border: 1px solid #e2e8f0;
        }
        .upload-group { display: flex; justify-content: space-between; gap: 15px; margin-bottom: 15px;}
        .person-box { 
            flex: 1; border: 2px dashed #cbd5e1; padding: 12px 10px; border-radius: 12px; 
            background: #f8fafc; transition: all 0.2s ease; position: relative; text-align: center;
        }
        .person-box:hover { border-color: #3b82f6; background: #eff6ff;}
        .person-box h4 { margin: 0 0 8px 0; color: #1e3a8a; font-size: 14px; font-weight: 700;}
        .name-input {
            width: 85%; padding: 6px 8px; margin: 4px auto; border: 1px solid #cbd5e1;
            border-radius: 6px; font-size: 12px; outline: none; text-align: center; display: block;
        }
        .name-input:focus { border-color: #3b82f6; }
        .qty-area {
            margin-top: 8px; background: #e2e8f0; padding: 6px; border-radius: 8px;
            display: flex; flex-direction: column; gap: 4px;
        }
        .qty-row { display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: bold; color: #334155;}
        .qty-row input { width: 45px; text-align: center; padding: 2px; border-radius: 4px; border: 1px solid #94a3b8; font-weight: bold;}
        .badge { color: white; padding: 2px 5px; border-radius: 4px; font-size: 10px;}
        .bg-3x4 { background: #2563eb; }
        .bg-4x6 { background: #16a34a; }
        input[type="file"] { display: none; }
        .custom-file-upload { 
            display: inline-block; padding: 6px 10px; cursor: pointer; background-color: #ffffff; 
            color: #475569; border-radius: 6px; font-weight: 600; font-size: 11px; 
            border: 1px solid #cbd5e1; width: 85%; margin: 0 auto;
        }
        .custom-file-upload:hover { background-color: #f1f5f9; }
        .img-wrapper { position: relative; display: inline-block; margin-top: 6px; }
        .preview { 
            max-width: 70px; max-height: 90px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); 
            border: 1px solid #fff; display: none; object-fit: cover;
        }
        .clear-btn { 
            position: absolute; top: -6px; right: -6px; background: #ef4444; color: white; 
            border: none; border-radius: 50%; width: 18px; height: 18px; font-size: 10px; 
            font-weight: bold; cursor: pointer; display: none; align-items: center; justify-content: center;
        }
        .btn-group { display: flex; gap: 10px; justify-content: center; margin-top: 20px;}
        .btn { 
            border-radius: 8px; padding: 12px 18px; font-size: 13px; font-weight: 700; 
            text-transform: uppercase; cursor: pointer; color: white; border: none; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: all 0.2s ease; flex: 1; 
        }
        #previewBtn { background: #2563eb; }
        #previewBtn:hover { background: #1d4ed8; }
        #downloadBtn { background: #16a34a; display: none; }
        #downloadBtn:hover { background: #15803d; }
        #directPrintBtn { background: #dc2626; display: none; }
        #directPrintBtn:hover { background: #b91c1c; }
        #previewContainer { display: none; margin-top: 25px; border-top: 2px dashed #e2e8f0; padding-top: 15px; }
        #previewContainer h4 { color: #334155; margin-bottom: 15px; font-weight: 700;}
        .a4-page-preview {
            position: relative; width: 100%; max-width: 480px; background: white; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin: 0 auto 20px auto; 
            border: 1px solid #94a3b8; overflow: hidden; border-radius: 4px;
        }
        .label-text-style {
            position: absolute; width: 100%; text-align: center; color: #1e293b;
            font-family: Arial, sans-serif; font-weight: bold; overflow: hidden; white-space: nowrap;
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <!-- Hàng 1 -->
        <div class="upload-group">
            <div class="person-box">
                <h4>👤 Người thứ 1</h4>
                <input type="text" id="name1" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput1" class="custom-file-upload" id="labelInput1">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput1" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview1" class="preview" alt="Preview 1"><button id="clearBtn1" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_1" value="9" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_1" value="0" min="0" max="24"></div>
                </div>
            </div>
            <div class="person-box">
                <h4>👤 Người thứ 2</h4>
                <input type="text" id="name2" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput2" class="custom-file-upload" id="labelInput2">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput2" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview2" class="preview" alt="Preview 2"><button id="clearBtn2" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_2" value="9" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_2" value="0" min="0" max="24"></div>
                </div>
            </div>
        </div>

        <!-- Hàng 2 -->
        <div class="upload-group">
            <div class="person-box">
                <h4>👤 Người thứ 3</h4>
                <input type="text" id="name3" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput3" class="custom-file-upload" id="labelInput3">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput3" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview3" class="preview" alt="Preview 3"><button id="clearBtn3" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_3" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_3" value="0" min="0" max="24"></div>
                </div>
            </div>
            <div class="person-box">
                <h4>👤 Người thứ 4</h4>
                <input type="text" id="name4" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput4" class="custom-file-upload" id="labelInput4">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput4" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview4" class="preview" alt="Preview 4"><button id="clearBtn4" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_4" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_4" value="0" min="0" max="24"></div>
                </div>
            </div>
        </div>

        <!-- Hàng 3 -->
        <div class="upload-group">
            <div class="person-box">
                <h4>👤 Người thứ 5</h4>
                <input type="text" id="name5" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput5" class="custom-file-upload" id="labelInput5">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput5" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview5" class="preview" alt="Preview 5"><button id="clearBtn5" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_5" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_5" value="0" min="0" max="24"></div>
                </div>
            </div>
            <div class="person-box">
                <h4>👤 Người thứ 6</h4>
                <input type="text" id="name6" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput6" class="custom-file-upload" id="labelInput6">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput6" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview6" class="preview" alt="Preview 6"><button id="clearBtn6" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_6" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_6" value="0" min="0" max="24"></div>
                </div>
            </div>
        </div>

        <!-- Hàng 4 -->
        <div class="upload-group">
            <div class="person-box">
                <h4>👤 Người thứ 7</h4>
                <input type="text" id="name7" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput7" class="custom-file-upload" id="labelInput7">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput7" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview7" class="preview" alt="Preview 7"><button id="clearBtn7" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_7" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_7" value="0" min="0" max="24"></div>
                </div>
            </div>
            <div class="person-box">
                <h4>👤 Người thứ 8</h4>
                <input type="text" id="name8" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput8" class="custom-file-upload" id="labelInput8">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput8" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview8" class="preview" alt="Preview 8"><button id="clearBtn8" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_8" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_8" value="0" min="0" max="24"></div>
                </div>
            </div>
        </div>

        <!-- Hàng 5 -->
        <div class="upload-group">
            <div class="person-box">
                <h4>👤 Người thứ 9</h4>
                <input type="text" id="name9" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput9" class="custom-file-upload" id="labelInput9">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput9" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview9" class="preview" alt="Preview 9"><button id="clearBtn9" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_9" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_9" value="0" min="0" max="24"></div>
                </div>
            </div>
            <div class="person-box">
                <h4>👤 Người thứ 10</h4>
                <input type="text" id="name10" class="name-input" placeholder="Nhập tên...">
                <label for="imgInput10" class="custom-file-upload" id="labelInput10">📁 Chọn Ảnh...</label>
                <input type="file" id="imgInput10" accept="image/png, image/jpeg, image/jpg">
                <center><div class="img-wrapper"><img id="preview10" class="preview" alt="Preview 10"><button id="clearBtn10" class="clear-btn">✖</button></div></center>
                <div class="qty-area">
                    <div class="qty-row"><span><span class="badge bg-3x4">3x4</span> SL:</span><input type="number" id="qty3x4_10" value="0" min="0" max="24"></div>
                    <div class="qty-row"><span><span class="badge bg-4x6">4x6</span> SL:</span><input type="number" id="qty4x6_10" value="0" min="0" max="24"></div>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button id="previewBtn" class="btn">👁️ Xem Trước Bản Xếp</button>
            <button id="downloadBtn" class="btn">⬇️ Tải Xuống PDF</button>
            <button id="directPrintBtn" class="btn">🖨️ Tiến Hành In</button>
        </div>
        <div id="previewContainer">
            <h4>📄 MÔ PHỎNG TRANG IN CHUẨN A4</h4>
            <div id="pdfIframeContainer"></div>
        </div>
    </div>

    <script>
        let dataStore = Array(11).fill(null);
        let typeStore = Array(11).fill('JPEG');

        function handleImageUpload(inputId, previewId, clearBtnId, labelId, personNum) {
            document.getElementById(inputId).addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    typeStore[personNum] = (file.type === 'image/png') ? 'PNG' : 'JPEG';

                    const reader = new FileReader();
                    reader.onload = function(event) {
                        dataStore[personNum] = event.target.result;

                        const imgElement = document.getElementById(previewId);
                        imgElement.src = event.target.result;
                        imgElement.style.display = 'block';
                        document.getElementById(clearBtnId).style.display = 'flex';
                        document.getElementById(labelId).innerHTML = '🔄 Đổi Ảnh';
                    }
                    reader.readAsDataURL(file);
                }
            });
            document.getElementById(clearBtnId).addEventListener('click', function() {
                document.getElementById(inputId).value = "";
                document.getElementById(previewId).style.display = 'none';
                document.getElementById(previewId).src = "";
                this.style.display = 'none';
                document.getElementById(labelId).innerHTML = '📁 Chọn Ảnh...';
                dataStore[personNum] = null;

                document.getElementById('previewContainer').style.display = 'none';
                document.getElementById('downloadBtn').style.display = 'none';
                document.getElementById('directPrintBtn').style.display = 'none';
            });
        }

        for(let i = 1; i <= 10; i++) {
            handleImageUpload(`imgInput${i}`, `preview${i}`, `clearBtn${i}`, `labelInput${i}`, i);
        }

        function getPersonsData() {
            let list = [];
            for(let i = 1; i <= 10; i++) {
                let q3x4 = parseInt(document.getElementById(`qty3x4_${i}`).value) || 0;
                let q4x6 = parseInt(document.getElementById(`qty4x6_${i}`).value) || 0;
                let pName = document.getElementById(`name${i}`).value.trim();
                if (dataStore[i] && (q3x4 > 0 || q4x6 > 0)) {
                    list.push({ data: dataStore[i], type: typeStore[i], qty3x4: q3x4, qty4x6: q4x6, name: pName });
                }
            }
            return list;
        }

        function buildLayoutData(persons) {
            const a4W = 210, a4H = 297;
            let gapX = 0.6, gapY = 0.6, marginX = 5, marginY = 3;
            let pages = [], currentPage = [], curX = marginX, curY = marginY;
            let maxRowHeight = 0;

            let allItems = [];
            persons.forEach((person) => {
                for (let i = 0; i < person.qty3x4; i++) {
                    allItems.push({ data: person.data, type: person.type, w: 30, h: 40, name: person.name });
                }
                for (let i = 0; i < person.qty4x6; i++) {
                    allItems.push({ data: person.data, type: person.type, w: 40, h: 60, name: person.name });
                }
            });

            allItems.forEach((item) => {
                if (curX + item.w > a4W - marginX) {
                    curX = marginX;
                    curY += maxRowHeight + gapY;
                    maxRowHeight = 0;
                }

                if (curY + item.h > a4H - marginY) {
                    pages.push(currentPage);
                    currentPage = [];
                    curX = marginX;
                    curY = marginY;
                    maxRowHeight = 0;
                }

                currentPage.push({ data: item.data, type: item.type, x: curX, y: curY, w: item.w, h: item.h, name: item.name });

                if (item.h > maxRowHeight) {
                    maxRowHeight = item.h;
                }

                curX += item.w + gapX;
            });

            if (currentPage.length > 0) pages.push(currentPage);
            return pages;
        }

        document.getElementById('previewBtn').addEventListener('click', function() {
            let persons = getPersonsData();
            if (persons.length === 0) return alert("Vui lòng tải ảnh lên và chọn số lượng!");
            let pages = buildLayoutData(persons);
            let pagesHtml = '';

            pages.forEach(page => {
                pagesHtml += `<div class="a4-page-preview" style="aspect-ratio: 210/297; border: 1px solid #777; background:#fff; margin-bottom:20px; position:relative;">`;
                page.forEach(img => {
                    let pLeft = (img.x / 210) * 100 + '%';
                    let pTop = (img.y / 297) * 100 + '%';
                    let pWidth = (img.w / 210) * 100 + '%';
                    let pHeight = (img.h / 297) * 100 + '%';
                    pagesHtml += `<img src="${img.data}" style="position: absolute; left: ${pLeft}; top: ${pTop}; width: ${pWidth}; height: ${pHeight}; object-fit: cover; border: 1px solid #E5E5E5; box-sizing: border-box;">`;
                    if (img.name) {
                        let labelTop = ((img.y + img.h - 3.2) / 297) * 100 + '%';
                        let labelFontSize = (img.w === 30) ? '8px' : '9px';
                        pagesHtml += `<div class="label-text-style" style="left: ${pLeft}; top: ${labelTop}; font-size: ${labelFontSize}; background: rgba(255,255,255,0.85); height:13px; line-height:13px;">${img.name}</div>`;
                    }
                });
                pagesHtml += `</div>`;
            });
            document.getElementById('pdfIframeContainer').innerHTML = pagesHtml;
            document.getElementById('previewContainer').style.display = 'block';
            document.getElementById('downloadBtn').style.display = 'inline-block';
            document.getElementById('directPrintBtn').style.display = 'inline-block';
        });

        function generateJsPDFObject() {
            let persons = getPersonsData();
            const { jsPDF } = window.jspdf;
            let doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
            let pages = buildLayoutData(persons);
            pages.forEach((page, pageIdx) => {
                if (pageIdx > 0) doc.addPage();
                page.forEach(img => {
                    doc.addImage(img.data, img.type, img.x, img.y, img.w, img.h);
                    doc.setDrawColor(225, 225, 225); doc.setLineWidth(0.08); doc.rect(img.x, img.y, img.w, img.h, 'S');
                    if (img.name) {
                        doc.setFillColor(255, 255, 255); doc.rect(img.x + 0.2, img.y + img.h - 3.0, img.w - 0.4, 2.8, 'F');
                        doc.setTextColor(60, 60, 60); let fSize = (img.w === 30) ? 5.5 : 6.5;
                        doc.setFontSize(fSize); doc.setFont("Helvetica", "bold");
                        doc.text(img.name, img.x + (img.w / 2), img.y + img.h - 0.8, { align: 'center' });
                    }
                });
            });
            return doc;
        }

        document.getElementById('downloadBtn').addEventListener('click', function() { generateJsPDFObject().save('SmartStudio_Print_Layout.pdf'); });
        document.getElementById('directPrintBtn').addEventListener('click', function() {
            let doc = generateJsPDFObject(); const blobUrl = doc.output('bloburl'); const printWindow = window.open(blobUrl, '_blank');
            if (printWindow) { printWindow.onload = function() { printWindow.focus(); printWindow.print(); }; }
            else { alert("Vui lòng cho phép Pop-up trên trình duyệt để mở hộp thoại in!"); }
        });
    </script>
</body>
</html>"""

components.html(html_code, height=1850, scrolling=True)
