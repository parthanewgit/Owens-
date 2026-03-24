import logging
import PyPDF2
from pathlib import Path
import os
import time

logger = logging.getLogger(__name__)

class ParserService:
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF"""
        
        logger.info(f"Parsing PDF: {file_path}")
        
        text = ""
        try:
            # Ensure file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Small delay to ensure file is fully written
            time.sleep(0.1)
            
            with open(file_path, 'rb') as file:
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    
                    if num_pages == 0:
                        logger.warning("PDF has no pages")
                        return "[Empty PDF]"
                    
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                    
                except Exception as inner_e:
                    logger.warning(f"PyPDF2 parsing issue: {str(inner_e)}")
                    # Return placeholder if parsing fails
                    text = "[PDF could not be fully parsed - content may be image-based]"
        
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise ValueError(f"Failed to parse PDF: {str(e)}")
        
        return text if text.strip() else "[PDF content extraction returned empty result]"
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX"""
        
        logger.info(f"Parsing DOCX: {file_path}")
        
        try:
            from docx import Document
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
            
            if not text.strip():
                logger.warning("DOCX file has no extractable text")
                return "[DOCX file is empty]"
            
            return text
            
        except ImportError:
            logger.error("python-docx not installed")
            raise ValueError("python-docx library is required for DOCX parsing")
        except Exception as e:
            logger.error(f"Error parsing DOCX: {str(e)}")
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
    
    @staticmethod
    def parse_text(file_path: str) -> str:
        """Extract text from TXT"""
        
        logger.info(f"Parsing TXT: {file_path}")
        
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            if not text.strip():
                logger.warning("TXT file is empty")
                return "[Empty text file]"
            
            return text
            
        except Exception as e:
            logger.error(f"Error parsing TXT: {str(e)}")
            raise ValueError(f"Failed to parse TXT: {str(e)}")
    
    @staticmethod
    def parse_resume(file_path: str) -> str:
        """Parse resume based on file type"""
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return ParserService.parse_pdf(file_path)
        elif file_ext == '.docx':
            return ParserService.parse_docx(file_path)
        elif file_ext == '.txt':
            return ParserService.parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}. Supported types: .pdf, .docx, .txt")
