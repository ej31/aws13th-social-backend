# 클라우드 커뮤니티 REST API Docs

<aside>
<img src="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" alt="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" width="40px" />

전체화면으로 해놓고 구현하시면 편합니다!
Cmd + T (Ctrl + T) 누르면 탭 추가가 가능합니다. 참고하세요!

창 추가하는건 Cmd + Shift + N (Ctrl + Shift + N) 입니다!.

</aside>

**Error Response ()**

```json
{
  "status": "error",
  "code": "",
  "message": ""
}
```

## Likes (좋아요)

### 내가 좋아요한 게시글 목록 조회

**GET** `/likes`

현재 로그인한 사용자가 좋아요를 누른 게시글 목록을 조회합니다. Authorization 헤더의 토큰을 통해 사용자를 식별합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 조회할 페이지 번호입니다.(기본값: 1) |
| limit | integer | X | 한 페이지에 표시할 개수입니다.(기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "likeId": 50,
      "postId": 10,
      "title": "좋아요한 게시글 제목",
      "nickname": "user",
      "createdAt": "2026-01-08T17:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "totalCount": 1,
    "totalPage": 1
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

---

### 좋아요 상태 확인

**GET** `/likes/status`

특정 게시글에 대한 총 좋아요 개수와 현재 로그인한 사용자의 좋아요 여부를 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | X | `Bearer {token}` 형식의 인증 정보입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 좋아요 상태를 확인할 게시글의 고유 식별자(ID)입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "postId": 10,
    "totalLikes": 125,
    "isLiked": true
  }
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

## Comments (댓글)

### 내가 쓴 댓글 목록

**GET** `/comments/me`

현재 로그인한 사용자가 작성한 모든 댓글을 모아서 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 조회할 페이지 번호입니다(기본값: 1) |
| limit | integer | X | 한 페이지에 표시할 댓글 개수입니다.(기본값: 10) |

**Response (200 OK)**

```json
{ 
  "status": "success",
  "data": [
    {
      "commentId": 15,
      "postId": 11,
      "postTitle": "AWS 수업",
      "content": "수고하셨습니다..",
      "createdAt": "2026-01-08T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "totalCount": 2,
    "totalPage": 1
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

---

### 댓글 목록 조회

**GET** `/comments`

특정 게시글에 달린 댓글들을 조회합니다. postId를 쿼리 파라미터로 받아 해당 게시글의 댓글 목록을 페이지네이션 형태로 변환합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | X | `Bearer {token}` 형식입니다. |
|  |  |  |  |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 댓글을 조회할 대상 게시글의 고유 식별자(ID)입니다. |
| page | integer | X | 조회할 페이지 번호입니다.(기본값: 1) |
| limit | integer | X | 한 페이지에 표시할 댓글 개수입니다.(기본값: 10) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "commentId": 1,
      "postId": 10,
      "content": "댓글입니다.",
      "userId": 1,
      "nickname": "user",
      "createdAt": "2026-01-08T16:40:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "totalCount": 1,
    "totalPage": 1
  }
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

## Posts (게시글)

### 게시글 정렬, 검색

**GET** `/posts`

특정 기준(최신순, 조회수순, 좋아요순)에 따라 정렬된 게시글 목록을 조회하고, 제목이나 내용에 특정 키워드가 포함된 게시글을 검색합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | X | Bearer {token} 형식의 인증 정보입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| sort | string | X | 정렬 기준입니다.(latest, views, likes) |
| page | integer | X | 조회할 페이지 번호입니다. |
| limit | integer | X | 페이지당 게시글 개수입니다. |
| key | string | X | 검색할 키워드입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "postId": 50,
      "title": "AWS S3 사용법 안내 (검색 결과)",
      "viewCount": 2500,
      "likeCount": 120,
      "nickname": "user123",
      "createdAt": "2026-01-08T10:00:00Z"
    }
  ],
  "meta": {
    "totalCount": 150,
    "currentPage": 1
  }
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "입력 데이터가 유효하지 않습니다. 필드 형식을 확인해주세요."
}
```

### 내가 쓴 게시글 목록 조회

**GET** `/posts/me`

현재 로그인한 사용자가 작성한 게시글들만 모아서 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. 본인을 식별하기 위해 필수입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 조회할 페이지 번호입니다.(기본값: 1) |
| limit | integer | X  | 한 페이지에 표시할 게시글 개수입니다.(기본값: 20) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "postId": 25,
      "title": "내가 오늘 작성한 글",
      "viewCount": 5,
      "likeCount": 1,
      "createdAt": "2026-01-08T16:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "totalCount": 2,
    "totalPage": 1
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

---

### 게시글 상세 조회

**GET** `/posts/{postId}`

특정 게시글의 상세 내용을 조회합니다. 이 API가 성공적으로 호출될 때마다 해당 게시글의 조회수가 자동으로 1씩 증가합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | X | `Bearer {token}` 형식의 인증 정보입니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 상세 조회할 게시글의 고유 식별자(ID)입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "postId": 10,
    "title": "게시글 상세 제목",
    "content": "이곳에 게시글의 전체 본문 내용이 들어갑니다. 여러 줄의 텍스트가 포함될 수 있습니다.",
    "nickname": "작성자닉네임",
    "profileImage": "https://example.com/profiles/img.png",
    "viewCount": 11,
    "likeCount": 11,
    "isLiked": false,
    "createdAt": "2026-01-08T12:00:00Z",
    "updatedAt": "2026-01-08T14:00:00Z"
  }
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 게시글 목록 조회

**GET** `/posts`

전체 게시글 목록을 조회합니다. 대량의 데이터를 효율적으로 처리하기 위해 페이지네이션을 지원하며, 제목이나 내용으로 검색하거나 다양한 기준으로 정렬할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | X | `Bearer {token}` 형식의 인증 정보입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 조회할 페이지 번호입니다.(기본값: 1) |
| limit | integer | X | 한 페이지에 표시할 게시글 개수입니다.(기본값: 20, 최대 100) |
| search | string | X | 검색어입니다. 제목 또는 내용에 포함된 키워드를 검색합니다. |
| sort | string | X | 정렬 기준입니다. latest(최신순), views(조회수순), likes(좋아요순)를 지원합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "postId": 1,
      "title": "게시글 제목입니다",
      "content": "게시글 본문 내용의 일부입니다",
      "nickname": "작성자닉네임",
      "viewCount": 10,
      "likeCount": 10,
      "createdAt": "2026-01-08T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "totalCount": 150,
    "totalPage": 8
  }
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "입력 데이터가 유효하지 않습니다. 필드 형식을 확인해주세요."
}
```

---

## Users (회원)

### 특정 회원 조회

**GET** `/users/{userId}`

다른 사용자의 공개 프로필 정보를 조회합니다. 목록 조회나 내 정보 조회와 달리 타인에게 공개 가능한 정보(닉네임, 프로필 이미지 등)만을 반환합니다. 존재하지 않는 사용자를 조회할 경우 404 에러가 반환됩니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O  | 로그인 시 발급 받은 AccessToken을 `Bearer {token}` 형태로 전달합니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| userId | int | O | 조회할 사용자의 고유 식별자(ID)입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "userId": 1,
    "nickname": "user",
    "profileImage": "https://example.com/profiles/img.png",
    "createdAt": "2025-12-25T10:00:00Z"
  }
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 내 프로필 조회

**GET** `/users/me`

로그인한 사용자 본인의 상세 프로필 정보를 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O  | Bearer 토큰 형식의 인증 정보. 로그인 시 발급받은 Access Token을 `Bearer {token}` 형태로 전달합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "userId": 1,
    "email": "user@example.com",
    "nickname": "user",
    "profileImage": "https://example.com/profiles/img.png",
    "createdAt": "2026-01-08T15:30:00Z"
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

---

## Likes (좋아요)

### 좋아요 삭제

**DELETE** `/posts/postId}/likes/me`

특정 게시글에 등록했던 좋아요를 취소(삭제)합니다.

**Request Headers**

| **헤더** | **타입** | **필수** | **설명** |
| --- | --- | --- | --- |
| Authorization | string | O | **`Bearer {token}`** 형식의 인증 정보입니다. |

**Path Parameters**

| **파라미터** | **타입** | **필수** | **설명** |
| --- | --- | --- | --- |
| postId | integer | O | 좋아요를 취소할 게시글의 고유 ID입니다. |

**Request Example** Body 없이 Query String을 사용합니다*.* `DELETE /posts/125/likes/me`

**Response (204 No Content)**

**본문 없음**

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 좋아요 등록

**POST** `/likes`

특정 게시글에 좋아요를 등록합니다. 이미 좋아요를 누른 상태라면 서버에서 중복 등록 방지 처리가 필요합니다.

**Request Headers**

| **헤더** | **타입** | **필수** | **설명** |
| --- | --- | --- | --- |
| Authorization | string | O | **`Bearer {token}`** 형식의 인증 정보입니다. |
| Content-Type | string | O | application/json |

**Request Body**

| **필드** | **타입** | **필수** | **설명** |
| --- | --- | --- | --- |
| postId | integer | O | 좋아요를 누를 게시글의 고유 ID입니다. |

**Request Example**

```json
{
  "postId": 125
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "message": "해당 게시글에 좋아요를 눌렀습니다.",
  "data": {
    "likeId": 789,
    "postId": 125,
    "userId": 1,
    "createdAt": "2026-01-10T12:10:00Z"
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

**Error Response (409 Conflict)**

```json
{
  "status": "error",
  "code": "ALREADY_LIKED",
  "message": "이미 좋아요를 누른 게시글입니다."
}
```

---

## Comments (댓글)

### 댓글 삭제

**DELETE** `/comments/{commentId}`

본인이 작성한 특정 댓글을 삭제합니다. 삭제 후에는 데이터를 복구할 수 없습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |

**Path Parameters**

| **파라미터** | **타입** | **필수** | **설명** |
| --- | --- | --- | --- |
| commentId | integer | O | 삭제할 댓글의 고유 ID입니다. |

**Response (204 No Content)**

```json
{
  "status": "success",
  "message": "댓글이 성공적으로 삭제되었습니다."
}
```

**Error Response (403 Forbidden)**

```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "해당 리소스에 대한 수정 및 삭제 권한이 없습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 댓글 수정

**PATCH** `/comments/{commentId`}

본인이 작성한 특정 댓글의 내용을 수정합니다. 작성자 본인 확인은 서버에서 토큰을 통해 검증합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |
| Content-Type | string | O | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| commentId | integer | O | 수정할 댓글의 고유 식별자(ID)입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | string | O | 변경할 새로운 댓글입니다. |

**Request Example**

```json
{
  "content": "변경할 댓글 내용입니다."
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "message": "댓글이 수정되었습니다.",
  "data": {
    "commentId": 456,
    "content": "변경한 댓글 내용입니다.",
    "updatedAt": "2026-01-10T11:00:00Z"
  }
}
```

**Error Response (403 Forbidden)**

```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "해당 리소스에 대한 수정 및 삭제 권한이 없습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 댓글 작성

**POST** `/comments`

새로운 댓글을 작성합니다. 어떤 게시글에 다는 댓글인지 `postId`를 통해 명시해야 합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 댓글을 작성할 게시글의 ID입니다. |
| content | string | O | 댓글 내용입니다. |

**Request Example → Reqeust Body 가 있는 경우 작성 필**

```json
{
  "postId": 125,
  "content": "댓글 내용입니다,"
}
```

**Response (201 Created) → 상황에 맞게 바꿔서 쓰세요.**

```json
{
  "status": "success",
  "message": "댓글이 성공적으로 등록되었습니다.",
  "data": {
    "commentId": 456,
    "postId": 125,
    "content": "댓글 내용입니다.",
    "nickname": "user",
    "createdAt": "2026-01-10T10:00:00Z"
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

## Posts (게시글)

### 게시글 삭제

**DELETE** `/posts/{postId}`

작성한 게시글을 삭제합니다. 본인(작성자)만 삭제할 수 있으며, 삭제된 데이터는 복구할 수 없습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 수정할 게시글의 고유 식별자(ID)입니다. |

**Response (204 No Content)**

```json
{
  "status": "success",
  "message": "게시글이 성공적으로 삭제되었습니다."
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (403 Forbidden)**

```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "해당 리소스에 대한 수정 및 삭제 권한이 없습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 게시글 수정

**PATCH** `/posts/{postId}`

기존에 작성한 게시글의 제목이나 내용을 수정합니다. 본인(작성자)만 수정할 수 있으며, 수정이 필요한 필드만 전송하면 됩니다

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string  | O | `Bearer {token}` 형식의 인증 정보입니다. |
| Content-Type | string | O | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | integer | O | 수정할 게시글의 고유 식별자(ID)입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | X | 변경할 새로운 제목입니다. |
| content | string | X | 변경할 새로운 본문 내용입니다. |

**Request Example**

```json
{
  "title": "수정된 제목",
  "content": "수정된 본문 내용"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "message": "게시글이 성공적으로 수정되었습니다.",
  "data": {
    "postId": 125,
    "title": "수정된 제목",
    "content": "수정된 본문 내용",
    "updatedAt": "2026-01-09T15:00:00Z"
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (403 Forbidden)**

```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "해당 리소스에 대한 수정 및 삭제 권한이 없습니다."
}
```

**Error Response (404 Not Found)**

```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "message": "요청하신 리소스를 찾을 수 없습니다."
}
```

---

### 게시글 작성

**POST** `/posts`

새로운 게시글을 작성합니다. 제목과 내용을 입력받으며, 작성자 정보는 인증 토큰에서 자동으로 추출하여 저장합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |
| Content-Type | string  | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | O | 게시글 제목입니다. |
| content | string  | O | 게시글의 본문 내용입니다. |

**Request Example**

```json
{
  "title": "게시글 제목 입력칸입니다.",
  "content": "게시글 본문 입력칸입니다."
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "message": "게시글이 성공적으로 등록되었습니다.",
  "data": {
    "postId": 125,
    "title": "게시글 제목입니다.",
    "content": "게시글 본문 내용입니다.",
    "nickname": "user",
    "viewCount": 0,
    "createdAt": "2026-01-09T14:00:00Z"
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "입력 데이터가 유효하지 않습니다. 필드 형식을 확인해주세요."
}
```

---

## Users (회원)

### 회원탈퇴

**DELETE** `/users/me`

현재 로그인한 사용자의 계정을 삭제하고 모든 개인정보를 삭제합니다. 본인 확인을 위해 현재 비밀번호를 필수로 입력받습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| password | string | O | 탈퇴 확인을 위한 사용자의 현재 비밀번호입니다. |

**Request Example → Reqeust Body 가 있는 경우 작성 필**

```json
{
  "password": "mypassword123!"
}
```

**Response (204 No Content)**

```json
{
  "status": "success",
  "message": "회원 탈퇴가 정상적으로 처리되었습니다. 그동안 이용해 주셔서 감사합니다."
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (403 Forbidden)**

```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "해당 리소스에 대한 수정 및 삭제 권한이 없습니다."
}
```

---

### 프로필 수정

**PATCH** `/users/me`

새로운 리소스를 생성합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | `Bearer {token}` 형식의 인증 정보입니다. |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | X | 새롭게 사용할 닉네임입니다. |
| profileImage | string(url) | X | 새롭게 등록할 프로필 이미지 URL입니다. |
| password | string | X | 변경할 새로운 비밀번호입니다. |
| currentPassword | string | X | 비밀번호 변경 시 본인 확인을 위한 기존 비밀번호입니다. |

**Request Example → Reqeust Body 가 있는 경우 작성 필**

```json
{
  "nickname": "user",
  "profileImage": "https://example.com/profiles/new-image.png",
  "password": "newpassword456!",
  "currentPassword": "password123!"
}
```

**Response (200 OK) → 상황에 맞게 바꿔서 쓰세요.**

```json
{
  "status": "success",
  "message": "프로필 정보가 성공적으로 수정되었습니다.",
  "data": {
    "userId": 1,
    "nickname": "개미왕",
    "profileImage": "https://example.com/profiles/new-image.png",
    "updatedAt": "2026-01-08T18:30:00Z"
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (403 Forbidden)**

```json
{
  "status": "error",
  "code": "FORBIDDEN",
  "message": "해당 리소스에 대한 수정 및 삭제 권한이 없습니다."
}
```

**Error Response (409 Conflict)**

```json
{
  "status": "error",
  "code": "DUPLICATE_RESOURCE",
  "message": "이미 사용 중인 정보(이메일/닉네임)입니다."
}
```

---

### 로그인

**POST** `/auth/tokens`

이메일과 비밀번호를 확인하여 사용자 인증을 진행하고, 서비스 이용에 필요한 액세스 토큰(JWT 등)을 발급합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 가입 시 등록한 이메일 주소입니다. |
| password | string | O | 사용자의 비밀번호입니다. |

**Request Example → Reqeust Body 가 있는 경우 작성 필**

```json
{
  "email": "user@example.com",
  "password": "password123!"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "message": "로그인에 성공하였습니다.",
  "data": {
    "userId": 1,
    "nickname": "user",
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "tokenType": "Bearer",
    "expiresIn": 3600
  }
}
```

**Error Response (401 Unauthorized)**

```json
{
  "status": "error",
  "code": "UNAUTHORIZED",
  "message": "인증 토큰이 누락되었거나 만료되었습니다."
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "입력 데이터가 유효하지 않습니다. 필드 형식을 확인해주세요."
}
```

---

### 회원가입

**POST** `/users`

서비스 이용을 위해 새로운 사용자로 등록합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 사용자의 이메일 주소(ID로 사용) |
| password | string | O | 사용자의 비밀번호(암호화하여 저장) |
| nickname | string | O | 서비스 내에서 표시될 닉네임 |
| profileImage | string(url) | X | 프로필 이미지 데이터(선택사항) |

**Request Example → Reqeust Body 가 있는 경우 작성 필**

```json
{
  "email": "user@example.com",
  "password": "password123!",
  "nickname": "user",
  "profileImage": "https://example.com/images/profile1.png"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "message": "회원가입이 완료되었습니다.",
  "data": {
    "userId": 1,
    "email": "user@example.com",
    "nickname": "user",
    "createdAt": "2026-01-08T17:30:00Z"
  }
}
```

**Error Response (409 Conflict)**

```json
{
  "status": "error",
  "code": "DUPLICATE_RESOURCE",
  "message": "이미 사용 중인 정보(이메일/닉네임)입니다."
}
```

**Error Response (422 Validation Error)**

```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "입력 데이터가 유효하지 않습니다. 필드 형식을 확인해주세요."
}
```

---