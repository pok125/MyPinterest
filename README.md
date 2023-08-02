# MyPinterest
## 배포 URL
* http://52.78.135.206/

## 프로젝트 개요
* 이미지와 텍스트로 자신의 Pin을 등록하고 그룹지어 사람들과 공유할 수 있는 서비스입니다.

## 프로젝트 목표
* generic view를 이용하여 빠르게 전체적인 기능 구현 (SSR)
* 일반 view로 전체코드 리팩토링 (SSR)
* Docker를 이용하여 서비스 배포
* Django ORM 쿼리 이해

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

## 배포 환경
1. 전체 구성

![Untitled (5)](https://github.com/pok125/MyPinterest/assets/26684769/01a4c522-72c0-450d-b383-5c898d8c2a98)

2. AWS Lightsail
   *  Ubuntu OS환경 VPC 인스턴스 사용
   *  서버 재시작 시, Public IP 자동 변경을 막기위해 고정 IP를 사용
   *  Tabby툴을 사용하여 서버 관리

3. Nginx

![Untitled (6)](https://github.com/pok125/MyPinterest/assets/26684769/3af41f1b-a689-4618-8978-007379f8d9e6)

   * HTML, CSS, JS, 이미지등 정적인 파일들을 클라이언트에게 전달하기 위해 Nginx 웹 서버 사용
   * 클라이언트와 통신하는 서버이며 요청에 대해 Django서버와 통신하며 처리
   * Nginx 웹 서버와 Django 서버 간의 통신을 위해 gunicorn WSGI 사용
   * Nginx 컨테이너와 Django 컨테이너 간의 통신을 위해 Docker Network를 이용하여 컨테이너 이름을 통해 통신

4. Docker
- Docker Volume

  ![Untitled (7)](https://github.com/pok125/MyPinterest/assets/26684769/4e00c7c5-18d9-4dc3-9f48-5cc2a27849e8)

  * 컨테이너 간 데이터 공유를 위해 Docker Volume 사용
  * Docker의 Volume파일을 통해 컨테이너 마다 데이터가 동기화 되기 때문에 컨테이너가 종료되어도 Volume파일은 유지 됩니다.

- Docker Stack
  * 컨테이너 형태로 서비스를 관리할 경우 컨테이너가 추가될 때마다 초기 세팅을 계속 해야하는 번거로움과 컨테이너가 다운됐을 시, 재부팅을 직접 해줘야 한다는 단점 때문에 
컨테이너들에 대한 초기 세팅을 한 번에 관리하고 각 컨테이너를 서비스로 관리하기 위해 Docker Stack을 사용하였습니다.
  * yml파일로 컨테이너들에 대한 초기 세팅 값들을 설정하여 처음 한 번 작성한 것으로 계속해서 컨테이너 추가가 가능합니다.
  * 각 컨테이너를 서비스로 관리하기 때문에 다운됐을 시 자동 재부팅이 됩니다. 또한 Scale-out도 가능합니다.

- Docker Secret
  * 보안상 민감한 키 값들을 Docker Secret을 이용하여 관리하였습니다.

- Docker Swarm
  * Docker Stack을 이용하기 위해 Swarm통해 클러스터 환경을 만들었습니다.

5. Portainer
   * Docker를 GUI로 관리하기 위해 사용
   * 모든 컨테이너들을 한 눈에 상태를 확인 가능하기 때문에 모니터링에 편리함을 느꼈습니다.

## 실행 페이지

1. 회원가입

![join](https://github.com/pok125/MyPinterest/assets/26684769/b7a1cdef-6fab-4253-99d3-f6c184272de0)

* AbstractUser를 상속받아 User모델을 커스텀하여 사용하였습니다.
* username이 아닌 email을 id값으로 변경하였습니다.
* UserCreationForm을 상속받아 해당 form으로 유효성 검사와 화면 구성을 하였습니다.
* 회원가입 시, user모델과 profile모델에 값이 저장됩니다. profile의 이미지의 경우 초기 빈 값으로 프론트에서 빈 값인 경우 static파일에서 image를 불러오도록 처리하였습니다.

2. 로그인, 로그아웃

![login](https://github.com/pok125/MyPinterest/assets/26684769/9b0cc9c4-f85a-49fe-827d-6e7cc2886db5)
![logout](https://github.com/pok125/MyPinterest/assets/26684769/71f675b1-991f-4fc3-8d0d-75e8b56bfb72)

* django auth에서 제공하는 login, authenticate, logout을 사용하였습니다.

3. 회원정보 수정, 회원탈퇴

![profile_update](https://github.com/pok125/MyPinterest/assets/26684769/27470fd4-407e-4073-9246-cdc8e9cc84ba)
![user_delete](https://github.com/pok125/MyPinterest/assets/26684769/90ba2b82-fd07-46c3-82df-6b8c2eb05f33)

* 해당 페이지는 로그인 유저, 비로그인 유저 다 접근 가능합니다.
* 로그인 유저: 해당 페이지의 유저와 동일한 유저인 경우 수정, 탈퇴 버튼이 활성화되고 다른 유저인 경우 팔로우 버튼이 활성화 됩니다.
* 비로그인 유저: 페이지 정보만 볼 수 있고 모든 버튼이 비활성화 됩니다.
* 수정과 탈퇴 요청인 경우, LoginRequiredMixin을 사용하여 비로그인 유저 처리를 하였고 요청을 보낸 유저와 탈퇴 시킬 유저가 동일하지 않다면 HttpResponseBadRequest로 처리하였습니다.

4. PinGroup 생성, 수정, 삭제
- pin 없을 때

![pingroup_create](https://github.com/pok125/MyPinterest/assets/26684769/08b2e3c0-75a3-4608-a48a-8e68a3b784c6)
![pingroup_update](https://github.com/pok125/MyPinterest/assets/26684769/60d3039a-7fc3-4ccc-963b-93deaf55cb57)
![pingroup_delete](https://github.com/pok125/MyPinterest/assets/26684769/aff967a0-7b5f-4da0-872a-71196e09e051)

- pin 있을 때

![pingroup_pinlist](https://github.com/pok125/MyPinterest/assets/26684769/95bab2e6-782f-439c-9012-16fcfa45fc36)
![pingroup_and_pin_delete](https://github.com/pok125/MyPinterest/assets/26684769/772276b6-ee42-42ab-918d-8726b7507dbb)

* pin을 생성하려면 pingroup을 선택하도록 Pin모델에 PinGroup을 ForeignKey로 설정 후 null=False 옵션을 두어 처리하였습니다.
* pingroup에 등록된 pin의 수를 모든 pingroup에 대해 pin들을 역참조로 조회 시 쿼리문이 계속 발생하는 N+1 문제를 발견하였습니다. 따라서 annotate와 Count를 이용하여 쿼리문을 한 번 호출하는 것으로 
문제를 해결하였습니다.
  
5. Pin 생성, 수정, 삭제

![pin_creates](https://github.com/pok125/MyPinterest/assets/26684769/fdef417a-df60-4c22-b4d7-d530279e8a88)
![pin_update](https://github.com/pok125/MyPinterest/assets/26684769/24bddb70-26e0-4bfc-9212-7a2083425b42)
![pin_delete](https://github.com/pok125/MyPinterest/assets/26684769/068fb2e7-3cfe-41f8-8eef-097fb8d9d476)

- Pin 상세 페이지 이동 경로
  * Pin메뉴, PinGroup 상세페이지

![pindetail_from_pinlist](https://github.com/pok125/MyPinterest/assets/26684769/14939221-8cde-43b0-8043-f4d47b5ce4f6)
![pindetail_from_pingroup](https://github.com/pok125/MyPinterest/assets/26684769/f6e4e1db-9b6b-4469-980a-8c2c6a71d39d)

* magic grid 오픈 소스를 이용하여 pin리스트 화면 구성을 하였습니다.
* 상세페이지에서 댓글에 대한 정보들을 가져올 때, N+1 문제를 발견하였습니다. select_related를 통해 정참조 join 쿼리를 통해 쿼리문을 한 번 호출하는 것으로 문제를 해결하였습니다.

6. 댓글 생성, 삭제

![comment_create_delete](https://github.com/pok125/MyPinterest/assets/26684769/e0cbe09f-9384-449e-851f-a30f39df761e)

7. 좋아요, 즐겨찾기, 팔로우

![like](https://github.com/pok125/MyPinterest/assets/26684769/782d0fba-c3b2-4b5d-b3fb-9fc60b19f796)
![bookmark](https://github.com/pok125/MyPinterest/assets/26684769/7ce87bf3-da72-4884-afe7-48d493d2c4fb)
![following](https://github.com/pok125/MyPinterest/assets/26684769/a75a4d80-a0bc-4f0a-beee-5d4635ab0f5d)

8. 로그인, 미로그인 유저

![pinlist_logout](https://github.com/pok125/MyPinterest/assets/26684769/bc235607-3df5-47c8-a59e-cf94bad789d1)
![pinlist_otheruser](https://github.com/pok125/MyPinterest/assets/26684769/a94d5b19-c62d-4e5b-aeb3-b96316f71751)

## 어려웠던 점
1. User모델 커스텀
  * 기본으로 제공되는 User모델에서 id를 username대신 email을 사용하고자 커스텀을 진행하였습니다. AbstractUser를 상속받아 User모델을 재정의하는 과정에서
username을 처리하는 과정에서 어려움을 겪었습니다. 이 과정에서 AbstractUser모델을 상속받아 커스텀 하려하면 User모델 뿐만아니라 UserManager class 또한 수정해야 한다는 것을 알게되었습니다.
또한 username을 명시하지 않아도 계속 기존 auth의 authenticate인증을 사용하려다 보니 email대신 username으로 처리되어 계속 인증에 실패하였습니다. 따라서 settings파일에
    
    ```
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_USERNAME_REQUIRED = False
    ```
    username대신 email을 쓰겠다는 것을 명시하여 해결하였습니다.

2. Django ORM 이해
  * 쿼리셋에 대해 실질적인 쿼리가 어떻게 수행되는지 알아보기 위해 logging과 pygments을 사용하였습니다. 실질적으로 쿼리문이 찍히는 것을 보니 기존에 생각하고 있던 실행 시점과 동작 방식이 전혀 다르다는 것을 알 수 있었습니다.
  ```
  a = 모델.objects.all()
  b = a[0]
  c = list(a)
  ```
위의 코드에서 all을 했을 때 db에서 모든 데이터를 가져오는 줄 알았지만 실질적으로 사용을 할 때 쿼리문이 동작하는 것을 알 수 있었습니다. 또한, b와 c 위의 코드에서 b,c 에서 두 번의 쿼리가 발생하게 됩니다. 하지만 c, b를 위치를 바꾸게 되면 
쿼리문은 c에서 한 번 발생합니다. 따라서 쿼리를 통해 가져온 데이터가 캐싱된다는 것을 확인 할 수 있었습니다. 이러한 이해를 토대로 작성했었던 코드들을 살펴보았고 N+1 쿼리가 발생하는 부분들을 발견하였고 annotate와 select_related를 이용하여
해결하였습니다. 그 밖에도 사용할 수 있는 함수들이 많이 있다는 것도 알게 되었습니다. 데이터가 적기 때문에 복잡한 쿼리문으로 쿼리 발생 빈도를 줄이는 것과 단순한 쿼리 여러번으로 처리하는 것에 대해 시간차이는 경험할 수 없었지만 장고의 쿼리 동작에 대해
이해할 수 있었습니다.

3. Docker를 이용한 배포
   
 
## 프로젝트를 마치며

