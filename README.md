# MyPinterest
## 프로젝트 개요
* Django를 이용하여 Pinterest서비스를 참고하여 만들어 배포까지 목표
## 프로젝트 목표
* generic view를 이용하여 빠르게 전체적인 기능 구현 (SSR)
* 일반 view로 전체코드 리팩토링 후 배포 (SSR)
* DRF를 이용하여 REST API 구현
## 개발환경
* Python 3.11.3
* asgiref 3.7.2
* beautifulsoup4 4.12.2
* Django 4.2.1
* django-bootstrap4 23.2
* Pillow 10.0.0
* python-decouple 3.8
* soupsieve 2.4.1
* sqlparse 0.4.4
## 앱 구성
* mycore(main)
* users
* profiles
* pins
* pingroups
* comments
## ERD
![Untitled (4)](https://github.com/pok125/MyPinterest/assets/26684769/edd7e9cb-2ddd-407b-bb7f-6ce2b1840092)

## 구현 기능
1. Secret 키 관리
```python
BASE_DIR = Path(__file__).resolve().parent.parent

# 최상위 폴더 경로
ROOT_DIR = os.path.dirname(BASE_DIR)

# secrets.json 경로
SECRETS_PATH = os.path.join(ROOT_DIR, 'secrets.json')

# settings모듈에 할당
secrets = json.loads(open(SECRETS_PATH).read())
for key, value in secrets.items():
    setattr(sys.modules[__name__], key, value)
```
2. 회원가입

![join](https://github.com/pok125/MyPinterest/assets/26684769/b7a1cdef-6fab-4253-99d3-f6c184272de0)

3. 로그인, 로그아웃

![login](https://github.com/pok125/MyPinterest/assets/26684769/9b0cc9c4-f85a-49fe-827d-6e7cc2886db5)
![logout](https://github.com/pok125/MyPinterest/assets/26684769/71f675b1-991f-4fc3-8d0d-75e8b56bfb72)

4. 회원정보 수정, 회원탈퇴

![profile_update](https://github.com/pok125/MyPinterest/assets/26684769/27470fd4-407e-4073-9246-cdc8e9cc84ba)
![user_delete](https://github.com/pok125/MyPinterest/assets/26684769/90ba2b82-fd07-46c3-82df-6b8c2eb05f33)

5. PinGroup 생성, 수정, 삭제
- pin 없을 때

![pingroup_create](https://github.com/pok125/MyPinterest/assets/26684769/08b2e3c0-75a3-4608-a48a-8e68a3b784c6)
![pingroup_update](https://github.com/pok125/MyPinterest/assets/26684769/60d3039a-7fc3-4ccc-963b-93deaf55cb57)
![pingroup_delete](https://github.com/pok125/MyPinterest/assets/26684769/aff967a0-7b5f-4da0-872a-71196e09e051)

- pin 있을 때

![pingroup_pinlist](https://github.com/pok125/MyPinterest/assets/26684769/95bab2e6-782f-439c-9012-16fcfa45fc36)
![pingroup_and_pin_delete](https://github.com/pok125/MyPinterest/assets/26684769/772276b6-ee42-42ab-918d-8726b7507dbb)

6. Pin 생성, 수정, 삭제

![pin_creates](https://github.com/pok125/MyPinterest/assets/26684769/fdef417a-df60-4c22-b4d7-d530279e8a88)
![pin_update](https://github.com/pok125/MyPinterest/assets/26684769/24bddb70-26e0-4bfc-9212-7a2083425b42)
![pin_delete](https://github.com/pok125/MyPinterest/assets/26684769/068fb2e7-3cfe-41f8-8eef-097fb8d9d476)

- Pin 상세 페이지 이동 경로
  1) Pin메뉴
  2) PinGroup 상세페이지

![pindetail_from_pinlist](https://github.com/pok125/MyPinterest/assets/26684769/14939221-8cde-43b0-8043-f4d47b5ce4f6)
![pindetail_from_pingroup](https://github.com/pok125/MyPinterest/assets/26684769/f6e4e1db-9b6b-4469-980a-8c2c6a71d39d)

7. 댓글

![comment](https://github.com/pok125/MyPinterest/assets/26684769/fb205339-b66b-45e4-a282-49d57127f1ab)

8. 로그인, 미로그인 유저

![pinlist_logout](https://github.com/pok125/MyPinterest/assets/26684769/bc235607-3df5-47c8-a59e-cf94bad789d1)
![pinlist_otheruser](https://github.com/pok125/MyPinterest/assets/26684769/a94d5b19-c62d-4e5b-aeb3-b96316f71751)
