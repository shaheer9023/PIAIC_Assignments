# CODE BREAKDOWN
---

### 1. **`from PyPDF2 import PdfReader`**
- **Kaam:**  
  Ye line `PyPDF2` library se `PdfReader` ko import kar rahi hai.  
  - **Maqsad:**  
    Iska kaam PDF file ko read karna aur usme se text extract karna hai.

---

### 2. **`from langchain_google_genai import ChatGoogleGenerativeAI`**
- **Kaam:**  
  Is line me `ChatGoogleGenerativeAI` ko import kiya gaya hai jo LangChain aur Google Gemini ko connect karta hai.  
  - **Maqsad:**  
    Ye function hum AI ko initialize karne ke liye use karte hain.

---

### 3. **`llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="AIzaSyCtrVX7O1eN87cAFOd8GdjrO0y_tLRPjtQ")`**
- **Kaam:**  
  - Is line me `ChatGoogleGenerativeAI` ka ek instance banaya gaya hai jise hum `llm` naam de rahe hain.  
  - `model="gemini-2.0-flash-exp"` ka matlab hai hum Gemini Flash 2.0 ka specific model use kar rahe hain.
  - `api_key` ke zariye Google Gemini API ko access diya ja raha hai.

  **Note:** API key real-world me kabhi expose nahi karni chahiye!

---

### 4. **`user_input = input("Enter your question: ")`**
- **Kaam:**  
  - User se input liya ja raha hai jo uska sawal hoga.  
  - Input function user ko prompt karta hai aur jo bhi wo type kare usse `user_input` variable me store karta hai.

---

### 5. **`pdf_path = "Panaversity Certified Agentic and Robotic AI Engineer.pdf"`**
- **Kaam:**  
  - PDF ka path set kiya ja raha hai jahan se hume document ko read karna hai.

---

### 6. **`pdf_reader = PdfReader(pdf_path)`**
- **Kaam:**  
  - `PdfReader` function PDF file ko open karta hai aur usse read karne ke liye ek object banata hai.  
  - Is object ko `pdf_reader` variable me store karte hain.

---

### 7. **`document = ""`**
- **Kaam:**  
  - Ek khaali string banayi gayi hai jisme hum PDF ka pura text store karenge.

---

### 8. **`for page in pdf_reader.pages:`**
- **Kaam:**  
  - Is loop ke zariye hum PDF ke har page ko ek ek karke iterate karte hain.

---

### 9. **`document += page.extract_text()`**
- **Kaam:**  
  - Har page se text extract karke `document` variable me add karte ja rahe hain.  
  - `+=` ka matlab hai ki naye text ko pehle wale text ke saath jodte jao.

---

### 10. **`instruction = f""" You have to guide the user according to the provided document... """`**
- **Kaam:**  
  - Ek string banayi ja rahi hai jisme AI ko instructions diye gaye hain:
    1. User ka sawal aur pura document diya gaya hai.
    2. Agar user ka sawal document ke bahar ka ho, to AI ko jawab dene se mana kar diya gaya hai.

---

### 11. **`response = llm.invoke(instruction)`**
- **Kaam:**  
  - `invoke` method ke zariye AI se instruction ke basis par jawab liya ja raha hai.  
  - `llm` object AI ko call karta hai aur instruction ke hisaab se response generate karta hai.

---

### 12. **`print(response.content)`**
- **Kaam:**  
  - AI se mila hua jawab print kiya ja raha hai.  
  - `response.content` me AI ka generated answer hota hai.

---

