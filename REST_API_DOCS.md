# 클라우드 커뮤니티 REST API Docs

<aside>
<img src="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" alt="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" width="40px" />

전체화면으로 해놓고 구현하시면 편합니다!
Cmd + T (Ctrl + T) 누르면 탭 추가가 가능합니다. 참고하세요!

창 추가하는건 Cmd + Shift + N (Ctrl + Shift + N) 입니다!.

</aside>

### 내가 좋아요한 게시글 목록

**GET** `/users/me/likes`

로그인한 사용자가 좋아요 누른 게시글 목록을 볼 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "게시물 제목",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

### 좋아요 상태 확인

**GET** `/posts/{post_id}/likes`

좋아요 상태를 확인할 수 있습니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | int | O | 좋아요 상태를 확인할 게시글 ID입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "is_liked": true,
    "total_count": 42
  }
}
```

**Response (500 Internal Error)**

```json
{
  "status": "error",
  "error": {
    "code": "**Internal Error**",
    "message": "인터넷이 연결되어 있지 않습니다",
    "details": {
		   "reason": "NETWORK_DISCONNECTED",
			 "hint": "서버에서 외부 API 요청 중 네트워크 연결 문제로 실패했습니다."
    }
  }
}
```

---

### 내가 쓴 댓글 목록

**GET** `/users/me/comments`

자신이 쓴 댓글 목록을 볼 수 있습니다..

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": "1",
      "nickname": "회원 닉네임",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

### 댓글 목록 조회

**GET** `/posts/{post_id}/comments?page=1&limit=10` 

댓글 목록을 조회하는 기능입니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `post_id` | int | O | 조회할 게시글 ID입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | X |  |
| limit | int | X |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": "1",
      "nickname": "회원 닉네임",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

### 내가 쓴 게시글 목록

**GET** `/users/me/posts`

자신이 쓴 게시글의 목록을 볼 수 있는 기능입니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "게시물 제목",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

### 게시글 상세 조회

**GET** `/posts/{post_id}`

게시글을 단건 조회합니다. 조회 성공 시 해당 게시글의 조회수(view_count)가 1 증가합니다

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `post_id` | int | O | 조회할 게시글 ID입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "게시글 제목",
    "content": "게시글 내용",
    "view_count": 101,
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

---

### 게시글 정렬

**GET** `/posts?sort=created_at` 

작성글의 시간 순서대로 게시글을 정렬하는 기능입니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **sort** | string | X | 최신 순서대로 게시글을 정렬합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "게시물 제목",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

### 게시글 검색

**GET** `/posts?keyword=검색어`

엔드포인트 설명을 작성해주세요

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| keyword | string  | O | 검색어(제목, 내용)을 통해 게시글을 검색합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "게시물 제목",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

### 게시글 목록 조회

**GET** `/posts?page=2&limit=10`

게시글 목록을 조회할 수 있는 기능입니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | X | 조회할 페이지 번호 (기본값: 1) |
| limit | int | X | 페이지 당 게시글 수 (기본값: 10) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "게시물 제목",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 2,
    "limit": 10,
    "total": 100
  }
}
```

---

### 특정 회원 조회

**GET** `/users/{user_id}`

다른 사용자의 프로필 조회합니다. 리소스가 존재하지 않는 경우 404 에러가 반환됩니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| user_id | string | O | 조회할 회원의 고유 식별자입니다. 문자열 형식이며, 리소성 시 자동으로 할당됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "id": "1",
      "nickname": "회원 닉네임",
      "profile_image": "회원 프로필 URL",
      "created_at": "2026-01-04T12:00:00Z"
	 }
}
```

**Response (404 NOT FOUND)**

```json
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "요청한 회원을 찾을 수 없습니다.",
    "details": {
	    "user_id": "123"
    }
  }
}
```

---

### 내 프로필 조회

**GET** `/users/me` 

로그인한 사용자 본인 정보를 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "email": "user@example.com",
      "nickname": "사용자 닉네임",
      "profile_image": "사용자 프로필 URL",
      "created_at": "2026-01-04T12:00:00Z"
    }
}
```

---

### 좋아요 취소

**DELETE** `/posts/{post_id}/likes`

등록한 좋아요를 취소합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | int | O | 좋아요를 취소할 게시글 ID입니다. |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

```json
(요청 본문 없음)
```

**Response (204 No Content)**

```json
(응답 본문 없음)
```

---

### 좋아요 등록

**POST** `/posts/{post_id}/likes`

게시글에 좋아요를 등록합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | int | O | 좋아요를 등록할 게시글 ID입니다. |

**Request Body**

```json
(요청 본문 없음)
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "post_id": 1,
    "user_id": 42,
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

---

### 댓글 삭제

**DELETE** `/comments/{comment_id}`

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment_id | int | O | 삭제할 댓글 ID입니다. |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body** 

```json
(요청 본문 없음)
```

**Response (204 No Content)**

```json
(응답 본문 없음)
```

**Response (400 BAD_REQUEST)**

```json
{
  "status": "error",
  "error": {
    "code": "BAD_REQUEST",
    "message": "comment_id는 1 이상의 정수여야 합니다",
    "details": {
    }
  }
}
```

---

### 댓글 수정

**PATCH** `/comments/{comment_id}`

자신이 작성한 댓글을 수정합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment_id | int | O | 수정할 댓글 ID |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | O | 수정할 댓글 |

**Request Body**

```json
{
  "comment": "수정할 댓글"
}
```

**Response (200 OK)** 

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "comment": "수정된 댓글",
      "updated_at": "2026-01-04T12:00:00Z"
    }
  ]
}
```

**Response (403 Forbidden)**

```json
{
  "status": "error",
  "error": {
    "code": "Forbidden",
    "message": "댓글을 수정할 권한이 없습니다.",
    "details": {
	    "comment_id" : "1"
    }
  }
}
```

---

### 댓글 작성

**POST** `/posts/{post_id}/comments`

게시글에 댓글을 답니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | int | O | 댓글을 작성할 게시글 |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | O | 작성할 댓글 |

**Request Body** 

```json
{
  "comment": "작성한 댓글",
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "comment": "게시글 댓글",
      "created_at": "2026-01-04T12:00:00Z"
    }
  ]
}
```

---

### 게시글 삭제

**DELETE**`/posts/{post_id}`

본인이 작성한 게시글만 삭제 가능합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | int | O | 삭제할 게시글 ID입니다. |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

```json
(요청 본문 없음)
```

**Response (204 No Content)**

```json
(응답 본문 없음)
```

---

### 게시글 수정

**PATCH**`/posts/{post_id}`

본인이 작성한 글만 수정 가능합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | int | O | 수정할 게시글 ID입니다. |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | O | 게시글의 제목 |
| content | string | O | 게시글의 내용 |

**Request Body**

```json
}
	"title": "게시글 제목",
  "content": "게시글 내용"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": "1",
	  "title": "게시글 제목",
    "content": "게시글 내용",
    "updated_at": "2026-01-04T12:00:00Z"
  }
}
```

**Response (401 UNAUTHORIZED)**

```json
{
  "status": "error",
  "error": {
    "code": "UNAUTHORIZED",
    "message": "인증이 필요합니다.",
    "details": {
    }
  }
}
```

---

### 게시글 작성

**POST**`/posts`

게시글(제목, 내용)을 작성합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | O | 게시글의 제목 |
| content | string | O | 게시글의 내용 |

**Request Body**

```json
{
	"title": "게시글 제목",
  "content": "게시글 내용"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": "1",
	  "title": "게시글 제목",
    "content": "게시글 내용"
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

**Response (422 Validation Error)**

```json
{
"status": "error",
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "요청 값이 유효하지 않습니다.",
    "details": {
      "title": "제목은 1자 이상 100자 이하여야 합니다.",
      "content": "내용은 필수 항목입니다."
    }
  }
}

```

---

### 회원 탈퇴

**DELETE**`/users/me` 

계정을 삭제합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| password | string | O | 계정 삭제 시 필요한 비밀번호 |

**Request Body**

```json
{
  "password": "password123"
}
```

**Response (204 No Content)**

```json
(응답 본문 없음)
```

---

### 프로필 수정

**PATCH** `/users/me`

닉네임, 프로필 이미지, 비밀번호를 변경합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | x | 변경할 사용자의 닉네임 |
| profile_image | string | x | 변경할 사용자의 프로필 이미지 |
| pasword | string | x | 변경할 사용자의 비밀번호 |

**Request Body**

```json
{
    "nickname": "변경할 닉네임",
    "profile_image": "변경할 프로필 이미지 URL",
    "password": "변경할 비밀번호"
}
```

**Response (200 OK))**

```json
{
  "status": "success",
  "data": {
    "id": "1",
    "nickname": "변경된 닉네임",
    "profile_image": "변경된 프로필 이미지 URL",
    "updated_at": "2026-01-04T12:00:00Z"
  }
}
```

---

### 로그인(토큰 발급)

**POST** `/auth/tokens`

이메일과 비밀번호로 인증 후 Access Token을 발급합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | `application/json` |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 사용자 이메일 |
| password | string | O | 사용자 비밀번호 |

```json
{
  "email": "asd[@example.com](mailto:jeff@example.com)",
  "password": "pass123!"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

**Response (401 Unauthorized)**

```json
{
  "status": "error",
  "error": {
    "code": "UNAUTHORIZED",
    "message": "이메일 또는 비밀번호가 일치하지 않습니다."
  }
}
```

**Response (422 Validation Error)**

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "요청 값이 유효하지 않습니다.",
    "details": {
      "email": "올바른 이메일 형식이 아닙니다."
    }
  }
}
```

---

### 회원가입

POST `/users`

회원가입을 할 수 있습니다 . email과 비밀번호, 닉네임과 프로필(이미지)로 가입을 할 수 있습니다.

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 사용자 이메일 |
| pasword | string | O | 사용자 비밀번호 |
| nickname | string | O | 사용자 닉네임 |
| profile_image | string | X | 프로필에 사용할 이미지 URL |

**Request** 

```json
{
  "email": "user@example.com",
  "pasword": "새 비밀번호",
  "nickname":"새 닉네임",
  "profile_image": "프로필 이미지 URL"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data":[
	 {
    "id": "1",
	  "email": "user@example.com",
    "nickname":"새 닉네임",
    "profile_image": "프로필 이미지 URL",
    "created_at": "2026-01-04T12:00:00Z"
   }
  ]
}
```

---