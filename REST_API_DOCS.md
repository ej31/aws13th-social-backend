# 클라우드 커뮤니티 REST API Docs

<aside>
<img src="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" alt="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" width="40px" />

전체화면으로 해놓고 구현하시면 편합니다!
Cmd + T (Ctrl + T) 누르면 탭 추가가 가능합니다. 참고하세요!

창 추가하는건 Cmd + Shift + N (Ctrl + Shift + N) 입니다!.

</aside>

공통적으로 발생하는 에러

**Error Response (500 Internal Error)**

```json
{
  "status": "error",
  "error": {
    "code": "Internal Error",
    "message": "서버 오류"
  }
}
```

---

### **내가 좋아요한 게시글 목록**

**GET** `/users/me/likes`

**내가 좋아요한 게시글 목록**: 로그인한 사용자가 좋아요 누른 게시글들 조회

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫 번째 페이지가 반환됩니다. (기본값: 1) |
| limit | integer | ❌ | 한 페이지에 보여줄 개수 최소 1, 최대 100까지 설정 가능합니다. (기본값: 10) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
    "id":1, 
    "title": "제목1",
    "nickname":"작성자 이름",
    },
    {
    "id":2, 
    "title": "제목2",
    "nickname":"작성자 이름",
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 형식의 요청 입니다."
  }
}
```

---

### **좋아요 상태 확인**

**GET** `/posts/{postId}/likes`

**좋아요 상태 확인**: 현재 사용자의 좋아요 여부 + 총 좋아요 수

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Path parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 게시글 ID |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "isLiked": true,
    "likeCount": 342
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

---

### **내가 쓴 댓글 목록**

**GET** `/users/me/comments` 

**내가 쓴 댓글 목록**: 로그인한 사용자의 댓글만 조회

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {accessToken} |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호 (기본값: 1) |
| limit | integer | ❌ | 페이지당 게시글 수. 1~100 (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "첫 번째 게시글",
      "nickname": "철수",
      "createdAt": "2026-01-06T09:15:00Z"
    },
    {
      "id": 2,
      "title": "두 번째 게시글",
      "nickname": "철수",
      "createdAt": "2026-01-07T14:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "UNAUTHORIZED",
    "message": "인증이 필요합니다. 유효한 토큰을 전달해 주세요."
  }
}
```

**Error Response (400 Bad Request)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

---

### **댓글 목록 조회**

**GET** `/posts/{postId}/comments`

**댓글 목록 조회**: 특정 게시글의 댓글 목록 (페이지네이션)

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 댓글을 조회할 원본 게시글의 ID |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫 번째 페이지가 반환됩니다. (기본값: 1) |
| limit | integer | ❌ | 한 페이지에 보여줄 댓글 수 최소 1, 최대 100까지 설정 가능합니다. (기본값: 10) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "content": "댓글 내용",
      "nickname": "고동희",
      "createdAt": "2026-01-06T09:15:00Z"
    },
    {
      "id": 2,
      "content": "댓글 내용",
      "nickname": "고동희",
      "createdAt": "2026-01-06T09:15:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 50
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

---

### **내가 쓴 게시글 목록**

**GET** `/users/me/posts`

**내가 쓴 게시글 목록**: 로그인한 사용자의 게시글만 조회

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫 번째 페이지가 반환됩니다. (기본값: 1) |
| limit | integer | ❌ | 한 페이지에 포함될 리소스 개수입니다. 최소 1, 최대 100까지 설정 가능합니다. (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
    "id":1, 
    "title": "제목1",
    "nickname":"고동희",
    "createdAt":"2026-01-06T09:15:00Z"
    },
    {
    "id":2 ,
    "title": "제목2",
    "nickname":"고동희",
    "createdAt":"2026-01-06T09:15:00Z"
   }
  ],
    "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

---

### **게시글 상세 조회**

**GET** `/posts/{postId}`

단건 조회 시 **조회수 자동 증가**

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 조회할 게시글의 고유 ID (식별자) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 10,
    "nickname": "김동희",
    "title": "제목",
    "content": "본문 내용",
    "viewCount": 101
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 형식의 요청 입니다."
  }
}
```

---

### **게시글 정렬**

**GET** `/posts`

게시글 정렬: 최신순, 조회수순, 좋아요순 등

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ❌ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. created_at:생성일 like_count:좋아요 개수 view_count:조회 횟수 (기본값:내림차순)으로 정렬됩니다. |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫 번째 페이지가 반환됩니다. (기본값: 1) |
| limit | integer | ❌ | 한 페이지에 포함될 리소스 개수입니다. 최소 1, 최대 100까지 설정 가능합니다. (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
    "id":1 ,
    "title": "제목1",
    "nickname":"김씨",
    "likeCount":0,
    "viewCount":76,
    "created_at":"2026-01-06T09:15:00Z"
    },
    {
    "id":2, 
   "title": "제목2",
    "nickname":"고씨",
    "likeCount":3,
    "viewCount":60,
    "createdAt":"2026-01-06T09:15:00Z"
   },
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

---

### **게시글** 제목/내용으로 검색

**GET** `/posts` 

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫 번째 페이지가 반환됩니다. (기본값: 1) |
| keyword | string | ❌ | 특정 단어로 검색합니다. |
| limit | integer | ❌ | 한 페이지에 포함될 리소스 개수입니다. 최소 1, 최대 100까지 설정 가능합니다. (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "nickname": "선씨",
      "title": "제목"
    },
    {
      "id": 2,
      "nickname": "고씨",
      "title": "제목"
    },
    {
      "id": 3,
      "nickname": "이씨",
      "title": "제목"
   },
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 3
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

---

### **게시글 목록 조회**

**GET** `/posts` 

페이지네이션 적용

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫 번째 페이지가 반환됩니다. (기본값: 1) |
| limit | integer | ❌ | 한 페이지에 포함될 리소스 개수입니다. 최소 1, 최대 100까지 설정 가능합니다. (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "nickname": "김씨",
      "title": "넘 졸림"
    },  
    {
      "id": 2,
      "nickname": "고씨", 
      "title": "가만히 앉아 있는거 지옥임"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}

```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

---

### **특정 회원 조회**

**GET** `/users/{id}` 

다른 사용자의 공개 프로필 조회

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ❌ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| id | integer | ✅ | 조회할 사용자의 고유 번호 |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 5,
    "nickname": "특정 사용자 이름",
    "profileImage": "https://api.com/img/face.png"
  }
}
```

**Error Response (403 FORBIDDEN)**

```json
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "접근 권한이 없습니다."
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

---

### **내 프로필 조회**

**GET** `/users/me` 

**내 프로필 조회**: 로그인한 사용자 본인 정보 조회

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "dong.hee4881@gmail.com",
    "nickname": "고동희",
    "profileImage": "https://api.com/img/face.png",
    "joinedAt": "2026-01-04T12:00:00Z"
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

---

### **좋아요 취소**

**DELETE**  `/posts/{postId}/likes`

**좋아요 취소**: 등록한 좋아요 취소

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Path parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 게시글 ID |

**Response (**204 No Content**)** 

```json
(응답 본문 없음)
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 형식의 요청 입니다."
  }
}
```

---

### **좋아요 등록**

POST`/posts/{postId}/likes`

**좋아요 등록**: 게시글에 좋아요 누르기 (로그인 필요)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Path parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 게시글 ID |

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "likeCount": 2      
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

---

### **댓글 삭제**:

**DELETE** `/posts/{postId}/comments/{commentId}`

**댓글 삭제**: 본인 작성 댓글만 삭제 가능

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

path parameters

| 피라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 게시글 ID |
| commentId | integer | ✅ | 삭제할 댓글 ID |

**Response (**204 No Content**)** 

```json
(응답 본문 없음)
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

---

### **댓글 수정**

**PATCH**  `/posts/{postId}/comments/{commentId}`

**댓글 수정**: 본인 작성 댓글만 수정 가능

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |
| Content-Type | string | ✅ |  application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 게시글 ID |
| commentId | integer | ✅ | 수정할 댓글의 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | String | ❌ | 댓글 내용  수정 |

**Request Example** 

```json
{
  "content": "댓글 내용 수정"
 
}
```

**Response (200 OK)** 

```json
{
  "status": "success",
  "data": {
    "id": 3,
    "nickname": "댓글 작성자",
    "content": "댓글 수",
     "updatedAt": "2026-01-08T12:00:00Z"
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }
}
```

---

### **댓글 작성**

**POST** `/posts/{postId}/comments`

**댓글 작성**: 게시글에 댓글 달기 (로그인 필요)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |
| Content-Type | string | ✅ |  application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 댓글을 조회할 원본 게시글의 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | String | ✅ | 댓글 내용 작성 |

**Request Example**

```json
{
  "content": "댓글 내용"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 3,
    "nickname": "댓글 작성자",
    "content": "댓글 내용임",
    "createdAt": "2026-01-08T12:00:00Z"
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

```json
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "접근 권한이 없습니다."
  }
}
```

---

### **게시글 삭제**

**DELETE** `/posts/{postId}`

**게시글 삭제**: 본인 작성 글만 삭제 가능

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 삭제할 게시글의 고유 ID (식별자) |

**Response (**204 No Content**)** 

```json
(응답 본문 없음)
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }

```

---

### **게시글 수정**

**PATCH** `/posts/{postId}`

**게시글 수정**: 본인 작성 글만 수정 가능

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |
| Content-Type | string | ✅ |  application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | String | ❌ | 게시글 제목 |
| content | String | ❌ | 게시글 본문 내용 |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | ✅ | 수정할 게시글의 고유 ID (식별자) |

**Request Example** 

```json
{
  "title": "제목",
  "content": "본문 내용"
}
```

**Response (200 ok)** 

```json
{
  "status": "success",
  "data": {
    "id": 23,
     "nickname": "고동희",
     "title": "제목 수정 완",
     "content": "본문 수정 완",
    "updatedAt": "2026-01-08T12:00:00Z"
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (404 NOT_FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "**NOT_FOUND**",
    "message": "요청하신 데이터를 찾을 수 없습니다."
  }

```

---

### **게시글 작성**

**POST** `/posts`

**게시글 작성**: 제목, 내용 입력 (로그인 필요)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |
| Content-Type | String | ✅ |  application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | String | ✅ | 게시글 제목 |
| content | String | ✅ | 게시글 본문 내용 |

**Request Example**

```json
{
  "title": "제목",
  "content": "본문 내용"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 23,
     "nickname": "고동희",
     "title": "제목",
     "content": "본문 내용"
    "createdAt": "2026-01-08T12:00:00Z"
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (403 FORBIDDEN)**

```json
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "접근 권한이 없습니다."
  }
}
```

---

### **회원 탈퇴**

**DELETE** `/users/me`

계정 삭제

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |

**Response (**204 No Content**)** 

```json
(응답 본문 없음)
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

---

### **프로필 수정**

**PATCH** `/users/me`

닉네임, 프로필 이미지, 비밀번호 변경

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증 정보. 로그인 시 발급 받은 Access Token을 Bearer {token} 형태로 전달합니다. |
| Content-Type | String | ✅ | multipart/form-data |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ❌ | 닉네임 변경 |
| password | string | ❌ | 비밀번호 변경 |
| profileImage | file | ❌ | 프로필 이미지 변경 |

**Request Example** 

```json
{
  "nickname": "김동희",
  "password": "rewq321!",
  "profileImage": "<FILE: new-profile.png>"
}
```

**Response (200 ok)** 

```json
{
  "status": "success",
  "data": {
    "id": 1,
     "nickname": "김동희",
     "profileImage": "https://api.com/img/new-face.png",
    "createdAt": "2026-01-04T12:00:00Z"
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "잘못된 형식의 값입니다.",
    "details": [
      {
        "field": "email",
        "issue": "이메일 형식이 아닙니다."
      },
      {
        "field": "password",
        "issue": "비밀번호는 8자 이상이어야 합니다."
      },
      {
        "field": "nickname",
        "issue": "닉네임은 13자 이하이어야 합니다."
      },
      {
        "field": "profileImage",
        "issue": "확장자는 jpg, jpeg, png만 가능합니다."
      }
    ]
  }
}
```

---

### 로그인

**POST** `/login`

**로그인**: 이메일/비밀번호로 인증 후 토큰 발급

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | ✅ |  application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | ✅ | 로그인에 필요한 email |
| password | string | ✅ | 로그인에 필요한 pw |

**Request Example** 

```json
{
  "email": "dong.hee4881@gmail.com",
  "password": "qwer123!"
}
```

**Response (200 ok)**

```json
{
  "status": "success",
  "data": {
    "accessToken": "token123",
    
    "user": {
      "id": 1,               
      "email": "dong.hee4881@gmail.com",
      "nickname": "고동희" 
     
    }
  }
}
```

**Error Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "**UNAUTHORIZED**",
    "message": "인증 실패"
  }
}
```

**Error Response (429 RATE_LIMITED)**

```json
{
  "status": "error",
  "error": {
    "code": "RATE_LIMITED",
    "message": "요청 횟수 제한을 초과했습니다. 잠시 후 다시 시도해주세요.",
    "details": [
      {
        "field": "retry_after",   
        "value": "60s",           
        "issue": "1분 뒤에 다시 시도할 수 있습니다."
      }
    ]
  }
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "잘못된 형식의 값 입니다.",
    "details": [
	    {"field": "email", "issue": "이메일 형식이 아닙니다."},
	    {"field": "password", "issue": "비밀번호는 8자 이상이어야 합니다."}
    ]
  }
}
```

---

### 회원가입

**POST** `/signup`

회원가입: 이메일/비밀번호/닉네임/프로필 이미지로 가

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | File | ✅ | multipart/form-data |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | ✅ | 이메일 형식으로 작성 |
| password | string | ✅ | 8자 이상의 문자열,특수문자를 사용 |
| nickname | string | ✅ | 1자 이상 13자 이하의 문자열,특수문자 사용 가능 |
| profileImage | File | ❌ | 확장자는 jpg, jpeg,png만 가능 사이즈는 500x500px 이상만 가능 |

**Request Example** 

```json
{
  "email": "dong.hee4881@gmail.com",
  "password": "qwer123!",
  "nickname": "고동희",
  "profileImage":"<FILE: profile.png>"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "dong.hee4881@gmail.com",
    "nickname":"고동희",
    "profileImage": "https://api.com/img/face.png",
    "createdAt": "2025-01-07T12:30:00Z"
  }
}
```

---

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "잘못된 형식의 값입니다.",
    "details": [
      {
        "field": "email",
        "issue": "이메일 형식이 아닙니다."
      },
      {
        "field": "password",
        "issue": "비밀번호는 8자 이상이어야 합니다."
      },
      {
        "field": "nickname",
        "issue": "닉네임은 13자 이하이어야 합니다."
      },
      {
        "field": "profileImage",
        "issue": "확장자는 jpg, jpeg, png만 가능합니다."
      }
    ]
  }
}
```

**Error Response (409 Conflict)**

```json
{
  "status": "error",
  "error": {
    "code": "**Conflict**",
    "message": "이미 존재하는 데이터가 있습니다.",
    "details": [
      {
        "field": "email",
        "issue": "이미 가입된 이메일 주소입니다."
      }
    ]
  }
}
```

**Error Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "잘못된 요청 형식입니다."
  }
}
```