import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("업무 지원 챗봇")
    
    # API 키 입력
    api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file:
            pdf_text = extract_text_from_pdf(uploaded_file)
            st.success("PDF 파일이 성공적으로 업로드되었습니다!")
            
            # 사용자 입력
            user_question = st.text_input("질문을 입력하세요:")
            
            if user_question:
                # PDF 내용을 컨텍스트로 추가하여 질문
                prompt = f"""
                다음 문서를 참고하여 질문에 답변해주세요:
                
                문서 내용:
                {pdf_text}
                
                질문: {user_question}
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.write("답변:", response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
