# cp1_style

---

## 코드스테이츠 CP1 프로젝트

### 이미지 및 리뷰데이터를 통한 의상 추천 서비스

### Crawling

#### scheduler를 이용해 메일 동작하게 됨.

### Cloud DB (Elephantsql)

#### model.py에 스키마가 작성되어 있음.

#### view.py에 DB에 자동 적재 되도록 연동. ( 해당 DB가 닫히면 다른 DB로 연동해야함 )

### Modeling

#### Recommend => Randomforest 를 사용해 사이즈 추천

#### What is that => Yolov5s를 이용해 object detect

### Django(WAS)

#### - CSS 파일 없이, html에 모든 스타일 작성.

#### - Cloud DB와 연동 ( ORM은 사용하지 않음 )

### AWS EC2(Deploy)

#### - AWS EC2 인스턴스 내부에 Docker Container를 동작시키고 포트포워딩.

#### - imgstyle.shop 으로 배포 진행. (현재는 DB 닫힘으로 인해 접속 불가)

# 동작

### 1. requirement.txt 내부 install 진행

### 2. manage.py 가 있는 폴더로 이동 후 CLI "python3 manage.py runserver" 를 진행하면 실행됨.

# 동작 예시
![의류 추천 서비스 시연](https://user-images.githubusercontent.com/65811799/200488047-752a57a2-91cb-48a6-855f-65cc1e0bb966.gif)

# Web 소개

### 1. Information : 각 메뉴에 대한 간략적 소개 작성

### 2. DashBoard : google data studio와 연동 시켜둠.

### 3. Recommend : USER 정보를 기입하면 ML모델을 통해 사이즈 추천 및 정보 + 추천된 사이즈를 통해서 결과 출력 ( 유저 정보 DB 자동 적재 )

### 4. What is that : 아무 이미지를 Drag and Drop 방식 혹은 해당 form 클릭 후 넣게 되면 DL 모델을 통해 입고 있는 옷의 정보를 토대로 제품 추천

### 5. Review : 성별 / ML / DL 에 대해서 리뷰를 받고 이를 통해 수정 및 보완이 필요한 부분을 확인. ( DB 자동 적재 )
