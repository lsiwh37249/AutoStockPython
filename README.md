### 기본 자동 매매(Show me the money)(SMTM)
1. 데이터 수집 : 가격 및 거래 정보, 뉴스, SNS 반응을 수집한다.
2. 데이터 분석 : 수집한 데이터를 분석하고 매매를 판단한다.
3. 거래 요청 및 처리 : 매매를 요청하고, 체결된 거래 정보를 처리한다.
4. 거래 내용 및 결과 분석 : 거래 내용과 결과를 데이터로 기록, 분석한다

### Streamlit 
```
$ streamlit run src/autostockpython/frontend/front_stream.py
```

### FastAPI
```
$uvicorn src.autostockpython.backend.backend_fast:app --reload
```

### Module
- Trader : 매매 정보를 VirtualMarket에 전송한다. 이 Trader 모듈은 매매 관련 정보를 전달하는 역할  Virtual Market은 매매 정보를 토대로 매매 API에 요청하는 역할을 한다. 이를 구분한 이유는 Trader가 모바일이 될 수도, 웹이 될 가능성을 열어두기 위함이다.  
