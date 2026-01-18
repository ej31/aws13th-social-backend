# Social Backend REST API 문서

클라우드 커뮤니티 서비스의 REST API 명세서입니다.

## 사용자(User) API

### { 내가 좋아요한 게시글 목록 }

**GET** `/users/me/likes`

로그인한 사용자가 좋아요를 누른 게시글 목록을 조회한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
|  |  |  |  |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 페이지 번호 (기본값: 1) |
| limit | integer | X | 페이지당 게시글 수 (기본값: 20) |
|  |  |  |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "postId": 5,
      "title": "좋아요 누른 게시글",
      "authorNickname": "kyunghk",
      "createdAt": "2026-01-04T10:00:00Z"
    },
    {
      "postId": 9,
      "title": "두 번째 좋아요 게시글",
      "authorNickname": "guest",
      "createdAt": "2026-01-03T14:40:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 좋아요 상태 확인 }

**GET** `/posts/{postId}/likes/status`

특정 게시글에 대해 현재 사용자의 좋아요 여부와 총 좋아요 수를 조회한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O  | Bearer |
|  |  |  |  |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 좋아요 상태를 확인할 게시글의 ID |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "liked": true,
    "likeCount": 12
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

**게시글이 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Post not found"
}
```

---

### { 내가 쓴 댓글 목록 }

**GET** `/users/me/comments`

로그인된 상태일 때의 내가 쓴 댓글만 조회할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
|  |  |  |  |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 페이지 번호 (기본값: 1) |
| limit | integer | X | 페이지당 댓글 수 (기본값: 20) |
|  |  |  |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 101,
      "postId": 5,
      "content": "내가 쓴 첫 댓글",
      "createdAt": "2026-01-04T12:30:00Z"
    },
    {
      "id": 108,
      "postId": 7,
      "content": "두 번째 댓글",
      "createdAt": "2026-01-03T18:20:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 내가 쓴 게시글 목록 }

**GET** `/users/me/posts` 

로그인한 사용자가 작성한 게시글 목록만 조회할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O  | Bearer |
|  |  |  |  |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 페이지 번호 (기본값: 1) |
| limit | integer | X | 페이지당 게시글 수 (기본값: 20) |
|  |  |  |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 8,
      "title": "내가 쓴 첫 게시글",
      "createdAt": "2026-01-04T10:00:00Z"
    },
    {
      "id": 12,
      "title": "두 번째 게시글",
      "createdAt": "2026-01-03T09:40:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 2
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 게시글 정렬 }

**GET** `/posts` 

게시글을 최신순, 조회수순, 좋아요순 등 기준으로 정렬하여 조회할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| sort | string | X | 정렬 기준 (latest, views, likes) |
| page | integer | X | 페이지 번호 (기본값: 1) |
| limit | integer | X | 페이지당 게시글 수 (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 5,
      "title": "조회수 많은 게시글",
      "authorNickname": "user",
      "createdAt": "2026-01-03T11:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 42
  }
}
```

**잘못된 정렬 기준 (400 Bad Request)**

```json
{
  "status": "error",
  "message": "Invalid sort option"
}
```

---

### { 게시글 검색 }

**GET** `/posts/search` 

제목 또는 내용을 기준으로 게시글을 검색할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| keyword | string | O | 검색 키워드 (제목/내용 기준) |
| page | integer | X | 페이지 번호 (기본값: 1) |
| limit | integer | X | 페이지당 게시글 수 (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 3,
      "title": "게시글 검색 테스트",
      "authorNickname": "user",
      "createdAt": "2026-01-05T09:10:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 8
  }
}

```

---

### { 특정 회원 조회 }

**GET** `/users/{userId}` 

특정 사용자의 공개 프로필 정보를 조회할 수 있습니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| userId | integer | O | 조회할 사용자의 ID |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 3,
    "nickname": "user",
    "profileImageUrl": "https://storage.googleapis.com/example-bucket/profile-images/sample-profile.jpg",
    "createdAt": "2026-01-02T08:20:00Z"
  }
}
```

**사용자가 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "User not found"
}
```

---

### { 댓글 목록 조회 }

**GET** `/posts/{postId}/comments` 

특정 게시글에 작성된 댓글 목록을 페이지네이션하여 조회할 수 있습니다. 

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 댓글을 조회할 게시글의 ID |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 페이지 번호 (기본값: 1) |
| limit | integer | X | 페이지당 댓글 수 (기본값: 20) |
|  |  |  |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 101,
      "content": "첫 번째 댓글입니다.",
      "authorNickname": "user",
      "createdAt": "2026-01-04T12:30:00Z"
    }    
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 5
  }
}

```

---

### { 게시글 상세 조회 }

**GET** `/posts/{postId}` 

특정 게시글의 상세 내용을 조회할 수 있습니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 조회할 게시글의 ID |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "첫 번째 게시글",
    "content": "게시글의 전체 내용입니다.",
    "authorNickname": "user",
    "createdAt": "2026-01-04T12:00:00Z"
  }
}
```

**게시글이 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Post not found"
}
```

---

### { 게시글 목록 조회 }

**GET** `/posts` 

전체 게시글을 페이지네이션하여 조회할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | x | 페이지 번호 (기본값: 1) |
| limit | integer | x | 페이지당 게시글 수 (기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "첫 번째 게시글",
      "authorNickname": "user",
      "createdAt": "2026-01-04T12:00:00Z"
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

---

### { 내 프로필 조회 }

**GET**  `/users/me`

로그인한 사용자 본인의 프로필 정보를 조회할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
|  |  |  |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "nickname": "user",
    "profileImageUrl": "https://storage.googleapis.com/example-bucket/profile-images/sample-profile.jpg",
    "createdAt": "2026-01-04T12:00:00Z"
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
"status":"error",
"message":"Authentication required"
}
```

---

### { 댓글 수정 }

**PATCH** `/comments/{commentId}`

로그인한 사용자가 본인이 작성한 댓글을 수정할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
| Content-Type | string | O | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| commentId | integer | O | 수정할 댓글의 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | string | O | 수정할 댓글 내용 |
|  |  |  |  |

**Request Example** 

```json
{
  "content": "수정된 댓글 내용입니다."
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 101,
    "content": "수정된 댓글 내용입니다.",
    "updatedAt": "2026-01-05T15:10:00Z"
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

**댓글이 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Comment not found"
}
```

**본인이 작성한 댓글이 아닌 경우 (403 Forbidden)**

```json
{
  "status": "error",
  "message": "You are not the author of this comment"
}
```

---

### { 게시글 수정 }

**PATCH `/posts/{postId}`**

로그인한 사용자가 본인이 작성한 게시글의 내용을 수정할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
| Content-Type | string | O | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 수정할 게시글의 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | X | 수정할 게시글 제목 |
| content | string | X | 수정할 게시글 내용 |

**Request Example** 

```json
{
  "title": "수정된 게시글 제목",
  "content": "수정된 게시글 내용입니다."
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 5,
    "title": "수정된 게시글 제목",
    "content": "수정된 게시글 내용입니다.",
    "updatedAt": "2026-01-05T14:20:00Z"
  }
}

```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

**게시글이 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Post not found"
}
```

**본인이 작성한 게시글이 아닌 경우 (403 Forbidden)**

```json
{
  "status": "error",
  "message": "You are not the author of this post"
}
```

---

### { 좋아요 취소 }

**DELETE `/posts/{postId}/likes`**

로그인한 사용자가 등록한 좋아요를 취소한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 좋아요를 취소할 게시글의 ID |

**Request Example** 

```json
DELETE /posts/1/likes
Authorization: Bearer {accessToken}

```

**좋아요를 누르지 않은 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Like not found"
}
```

**게시글이 없는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Post not found"
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 좋아요 등록 }

**POST** `/posts/{postId}/likes`

로그인한 사용자가 게시글에 좋아요를 등록할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 좋아요를 누를 게시글의 ID |
|  |  |  |  |

**Request Example** 

```json
POST /posts/1/likes
Authorization: Bearer {accessToken}
```

**Response (201 Created)** 

```json
{
  "status": "success"
}
```

**이미 좋아요를 누른 경우 (409 Conflict)**

```json
{
  "status": "error",
  "message": "Already liked"
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 댓글 삭제 }

**DELETE** `/comments/{commentId}`

로그인한 사용자가 본인이 작성한 댓글을 삭제할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| commentId | integer | O | 삭제할 댓글의 ID |
|  |  |  |  |

**Request Example**

```json
DELETE /comments/101
Authorization: Bearer {accessToken}
```

**댓글이 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Comment not found"
}
```

**본인이 작성한 댓글이 아닌 경우 (403 Forbidden)**

```json
{
  "status": "error",
  "message": "You are not the author of this comment"
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 댓글 작성 }

POST `/posts/{postId}/comments`

로그인한 사용자가 게시글에 댓글을 작성할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
| Content-Type | string | O | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 댓글을 작성할 게시글의 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | string | O | 댓글 내용 |
|  |  |  |  |

**Request Example** 

```json
{
  "content": "첫 번째 댓글입니다."
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 101,
    "content": "첫 번째 댓글입니다.",
    "authorNickname": "user",
    "createdAt": "2026-01-04T12:30:00Z"
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
"status":"error",
"message":"Authentication required"
}
```

**게시글이 존재하지 않는 경우 (404 Not Found)**

```json
{
"status":"error",
"message":"Post not found"
}
```

---

### { 게시글 삭제 }

**DELETE** `/posts/{postId}`

로그인한 사용자가 본인이 작성한 게시글을 삭제할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 삭제할 게시글의 ID |

**Request Example**

```json
DELETE /posts/1
Authorization: Bearer
```

**게시글이 존재하지 않는 경우 (404 Not Found)**

```json
{
  "status": "error",
  "message": "Post not found"
}
```

**본인이 작성한 게시글이 아닌 경우 (403 Forbidden)**

```json
{
  "status": "error",
  "message": "You are not the author of this post"
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 게시글 작성 }

**POST** `/posts`

로그인한 사용자가 제목과 내용을 입력하여 게시글을 작성할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | O | 게시글 제목 |
| content | string | O | 게시글 내용 |

+**Request Example → Request Body 가 있는 경우 작성 필수**

```json
{
  "title": "첫 번째 게시글",
  "content": "게시글 내용입니다."
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "첫 번째 게시글",
    "content": "게시글 내용입니다.",
    "authorNickname": "user",
    "createdAt": "2026-01-04T12:00:00Z"
  }
}
```

**Response (401** Unauthorized**)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 회원 탈퇴 }

**DELETE** `/users/me`

로그인한 사용자 계정을 삭제할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | bearer |

**Request Example** 

```json
DELETE /users/me
Authorization: Bearer {accessToken}
```

**Response (204 No Content)**

**이미 탈퇴한 사용자 / 사용자 없음 (404 Not Found)**

```json
{
  "status": "error",
  "message": "User not found"
}

```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
  "status": "error",
  "message": "Authentication required"
}
```

---

### { 프로필 수정 }

**PATCH `/users/me`**

로그인한 사용자의 닉네임, 프로필 이미지, 비밀번호를 수정할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | X | 변경할 닉네임 |
| profileImageUrl | string | X | 변경할 프로필 이미지 URL |
| password | string | X | 변경할 비밀번호 |

**Request Example**

```json
{
  "nickname": "new_nickname",
  "profileImageUrl": "https://storage.googleapis.com/example-bucket/profile-images/new-profile.jpg"
}

```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "nickname": "new_nickname",
    "profileImageUrl": "https://storage.googleapis.com/example-bucket/profile-images/new-profile.jpg",
    "updatedAt": "2026-01-05T10:15:00Z"
  }
}
```

**인증되지 않은 경우 (401 Unauthorized)**

```json
{
"status":"error",
"message":"Authentication required"
}
```

---

### { 로그인 }

**POST** `/users/login`

이메일과 비밀번호를 검증하여 인증 토큰을 발급할 수 있습니다. 

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string  | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 사용자 이메일 |
| password | string | O | 사용자 비밀번호 |

**Request Example**

```json
{
  "email": "user@example.com",
  "password": "password1"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "accessToken": "eDhsWUfjAqwoEWCnSj...",
    "tokenType": "Bearer"
  }
}
```

**Response (401** Unauthorized**)**

```json
{
  "status": "error",
  "message": "Invalid email or password"
}
```

---

### { 회원가입 }

**POST** `/users/sign-up`

이메일,비밀번호, 닉네임 정보를 입력받아 새로운 사용자 계정을 생성할 수 있습니다. 

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 사용자 이메일 |
| password | string | O | 비밀번호 |
| nickname | string | O | 사용자 닉네임 |
| profileImageUrl | string | X | 프로필 이미지 URL |

**Request Example**

```json
{
  "email": "user@example.com",
  "password": "password1",
  "nickname": "user",
  "profileImageUrl": "https://storage.googleapis.com/my-bucket/users/profile/profile.png"
}

```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "nickname": "user",
	  "profileImageUrl": "https://storage.googleapis.com/my-bucket/users/profile/profile.png",
    "createdAt": "2026-01-04T12:00:00Z"
  }
}
```
