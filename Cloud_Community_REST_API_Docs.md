# 클라우드 커뮤니티 REST API Docs

### 내가 좋아요한 게시물 목록

**GET** `/users/me/likes` 

로그인한 사용자가 좋아요 누른 게시글들 조회합니다. 이 엔드포인트는 시스템에 등록된 전체 리소스를 페이지네이션 형태로 반환합니다. 대량의 데이터를 효율적으로 처리하기 위해 `page`와 `limit` 파라미터를 활용하여 원하는 범위의 데이터만 요청할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며 지정하지 않으면 첫번째 페이지가 반환됩니다.(기본값: 1) |
| limit | integer | ❌ | 한 페이지에 포함될 좋아요 누른 게시물 개수입니다. 최소 1개, 최대 100개까지 설정 가능합니다.(기본값: 20) |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. liked_at(좋아요 누른 시간 기준) 또는 created_at(좋아요 누른 게시물 생성일 기준)으로 지정할 수 있으며 기본적으로 내림차순(좋아요 누른 순)으로 정렬됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "title": "게시글 제목",
      "like_count": "게시글 좋아요 수",
      "created_at": "내가 좋아요 누른 게시물 생성일자"
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

**GET** `/users/{nickname}/posts/likes` 

현재 사용자의 모든 게시물의 좋아요 여부와 총 좋아요 수를 조회합니다. 이 엔드포인트는 시스템에 등록된 전체 좋아요를 페이지네이션 형태로 반환합니다. 대량의 데이터를 효율적으로 처리하기 위해 `page`와 `limit` 파라미터를 활용하여 원하는 범위의 데이터만 요청할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫번째 페이지가 반환됩니다.(기본값: 1) |
| limit | integer | ❌ | 한 페이지에 포함될 좋아요 수가 표시된 게시물 개수입니다. 최소 1개, 최대 100개까지 설정 가능합니다.(기본값: 20) |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. `created_at`(생성일 기준) 또는 `like_total`(좋아요 수 기준)으로 지정할 수 있으며 기본적으로 내림차순(최신순)으로 정렬됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "title": "게시글 제목",
      "like_count": "게시물 좋아요 수",
      "like_total": "총 좋아요 수",
      "created_at": "2026-01-06T12:00:00Z"
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

### 내가 쓴 댓글 목록

**GET** `/users/{nickname}/comments` 

로그인한 회원에 한해서 본인이 쓴 모든 댓글을 조회합니다. 이 엔드포인트는 시스템에 등록된 전체 댓글을 페이지네이션 형태로 반환합니다. 대량의 데이터를 효율적으로 처리하기 위해 page와 limit 파라미터를 활용하여 원하는 범위의 데이터만 요청할 수 있습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | 로그인을 확인을 위한 인증 정보입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명                                                                                               |
| --- | --- | --- |--------------------------------------------------------------------------------------------------|
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며, 지정하지 않으면 첫번째 페이지가 반환됩니다. (기본값: 1)                                       |
| limit | integer | ❌ | 한 페이지에 표시될 댓글 개수입니다. 최소 1개, 최대 100개까지 설정 가능합니다. (기본값: 20)                                        |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. created_at(생성일 기준) 또는 like_count(공감 수 기준)을 지정할 수 있으며, 기본적으로 내림차순(최신순)으로 정렬됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "comment_id": "098765431",
      "comment": "댓글 내용",
      "like_count": "댓글 공감 수",
      "comment_created_at": "2026-01-04T12:00:00Z"
      }
  ], 
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 300
  }
}
```

---

### 댓글 목록 조회

**GET** `/posts/{post_id}/comments` 

특정 게시글의 댓글 목록을 조회합니다. 이 엔드포인트는 시스템에 등록된 전체 리소스를 페이지네이션 형태로 반환합니다. 대량의 데이터를 효율적으로 처리하기 위해 `page`와 `limit` 파라미터를 활용하여 원하는 범위의 데이터만 요청할 수 있습니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | integer | ✅ | 특정 게시물의 고유 식별자입니다. 해당 ID 리소스가 존재해야 조회가 됩니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명                                                                                                        |
| --- | --- | --- |-----------------------------------------------------------------------------------------------------------|
| page | integer | ❌ | 조회할 페이지 번호입니다. 첫번째 페이지가 반환됩니다.                                                                            |
| limit | integer | ❌ | 한 페이지에 포함될 댓글 개수입니다. 최소 1개, 최대 100개까지 설정 가능합니다.                                                           |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. `created_at`(생성일 기준) 또는 `like_count`(댓글 공감 수 기준)으로 지정할 수 있습니다. 기본적으로 내림차순(최신순)으로 정렬됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "post_id": "1234567890",
      "nickname": "닉네임",
      "comment": "댓글 내용",
      "like_count": "댓글 공감 수",
      "comment_created_at": "2026-01-06T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "comment_total": 1024
  }
}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

---

### 내가 쓴 게시글 목록

**GET** `/users/me/posts` 

내가 작성한 게시물을 모아서 볼 수 있습니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ✅ | 게시글 작성자의 고유 식별자입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "post_id": [
        "14567890",
        "14567891"
      ],
      "nickname": "닉네임",
      "title": "게시글 제목1, 게시글 제목2",
      "created_post_at": "2026-01-04T12:00:00Z"
    }
}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

**Error (422 Validation Error)**

```json
{
    "status": "error",
    "error": {
        "code": "VALIDATION ERROR",
        "message": "유효성 검사에서 실패하였습니다. 처리할 수 없는 엔티티입니다.",
        "details": {}
    }
}
```

---

### 게시글 상세 조회

**GET** `/posts/{post_id}`

특정 게시글의 상세 정보를 조회합니다.  단건 조회 시 조회수가 자동으로 증가합니다. 목록 조회에는 제공되지 않는 `content` 등의 추가 필드를 포함한 전체 정보를 반환합니다.

**Path Parameters**

| 파라미터    | 타입 | 필수 | 설명 |
|---------| --- | --- | --- |
| post_id | integer | ✅ | 조회할 게시글의 고유 식별자입니다. 게시글 생성 시 자동으로 할당됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "post_id": "1234567890",
      "nickname": "닉네임",
      "title": "게시글 제목",
      "post": "게시글 내용",
      "created_post_at": "2026-01-04T12:00:00Z",
      "post_update_at": "2026-01-04T12:00:00Z"
    }
}
```

**Error (400)**

```json
{
    "status": "error",
    "error": {
        "code": "BAD REQUEST",
        "message": "잘못된 요청입니다. 다시 확인하시고 사용해주세요.",
        "details": {}
    }
}
```

---

### 게시글 정렬(게시글 목록 조회와 기능이 겹치므로 통합 요)

**GET** `/posts` 

최신순, 조회수순, 좋아요순으로 게시글을 정렬합니다. 이 엔드포인트는 시스템에 등록된 전체 게시글을 페이지네이션 형태로 반환합니다. 대량의 데이터를 효율적으로 처리하기 위해 `page`와 `limit` 파라미터를 활용하여 원하는 범위의 데이터만 효청할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며 지정하지 않을 경우, 첫 페이지가 반환됩니다. (기본값: 1) |
| limit | integer | ❌ | 한 페이지에 포함될 리소스 개수입니다. 최소 1개, 최대 100까지 설정 가능합니다.(기본값: 20) |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. `created_at`(생성일 기준), `view`(조회수 기준), `like`(좋아요 수 기준)으로 지정할 수 있으며 기본적으로 내림차순(최신순)으로 정렬됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "nickname": "닉네임",
      "title": "게시글 제목",
      "like_count": "게시글 좋아요 수",
      "created_post_at": "2026-01-06T12:00:00Z"
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

**GET** `/posts/posts?search=키워드&search_type=title` 

제목이나 내용으로 특정 게시글을 조회합니다. 목록 조회에서는 제공되지 않는 `content` 필드를 포함한 전체 정보를 반환합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | ✅ | 조회할 게시물의 식별자입니다. `title`과 `content` 둘 중 하나만 무조건 입력해야 합니다. |
| content | string | ✅ | 조회할 게시물의 식별자입니다. `title`과 `content` 둘 중 하나만 무조건 입력해야 합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "nickname": "닉네임",
      "title": "게시글 제목",
      "post": "게시글 내용",
      "created_post_at": "2026-01-04T12:00:00Z"
    }
}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

---

### 게시글 목록 조회

**GET** `/posts`

모든 게시글 제목을 조회합니다. 이 엔드포인트는 시스템에 등록된 전체 게시글을 페이지네이션 형태로 반환합니다. 대량의 데이터를 효율적으로 처리하기 위해 `page`와 `limit` 파라미터를 활용하여 원하는 범위의 데이터만 요청할 수 있습니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | ❌ | 조회할 페이지 번호입니다. 1부터 시작하며 지정하지 않으면 첫번째 페이지가 반환됩니다.(기본값: 1) |
| limit | integer | ❌ | 한 페이지 당 보여지는 계정 개수입니다. 최소1, 최대 100까지 설정 가능합니다.(기본값: 20) |
| sort | string | ❌ | 결과 정렬 기준 필드입니다. `create_at`(생성일 기준) 또는  `updated_at`(수정일 기준)을 지정할 수 있습니다. 기본적으로 내림차순(최신순)으로 정렬됩니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "nickname": "닉네임",
      "title": "게시글 제목",
      "created_post_at": "2026-01-06T12:00:00Z",
      "updated_post_at": "2026-01-06T12:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

**Error (500 Internal Server Error)**

```json
{
    "status": "error",
    "error": {
        "code": "500 INTERNAR_SERVER_ERROR",
        "message": "서버에 예상치 못한 상황이 발생했습니다. 잠시 후 다시 시도해주세요.",
        "details": {}
    }
}
```

---

### 특정 회원 조회

**GET** `/users/{nickname)`

다른 사용자의 공개 프로필을 조회합니다. 비밀번호는 제공하지 않습니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ✅ | 조회할 리소스의 고유 식별자입니다.  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "nickname": "닉네임",
      "profile_image": "프로필 사진",
      "created_at": "2026-01-06T12:00:00Z"
    }
}
```

**Error (400 Bad Request)**

```json
{
    "status": "error",
    "error": {
        "code": "BAD REQUEST",
        "message": "잘못된 요청입니다. 다시 확인하시고 사용해주세요.",
        "details": {}
    }
}
```

---

### 내 프로필 조회

**GET** `/users/{nickname}`

로그인된 닉네임에 해당하는 사용자 정보를 조회합니다. 단 비밀번호는 제외하고 조회합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ✅ | 조회할 회원 정보의 고유 식별자입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "email": "이메일",
      "nickname": "닉네임",
      "profile_image": "프로필 이미지",
      "created_at": "2026-01-04T12:00:00Z"
    }
}
```

---

### 좋아요 취소

DELETE `/posts/{post_id}/likes`

기존에 눌렀던 게시글의 좋아요를 번복합니다. 좋아요를 취소하더라도 다시 좋아요를 등록할 수 있습니다.

Path Parameter

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | integer | ✅ | 좋아요를 취소할 게시글의 고유 식별자입니다. 게시글 생성 시 자동으로 할당됩니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| like | boolean | ✅ | 좋아요를 취소합니다. 취소 시 게시물에서 좋아요가 1 줄어듭니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data":{
        "title": "게시글 제목",
      "like_count": "1 줄어든 게시물 좋아요 수",
      "created_at": "내가 좋아요 누른 게시물 생성일자"
    }
}
```

**Error (204 Not Content)**

```json

```

---

### 좋아요 등록

**POST**`/posts/{post_id}/likes`

로그인을 했을 때 게시글에 좋아요를 누를 수 있습니다. 좋아요는 한 게시물에 한 번만 적용됩니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | 로그인 확인을 위한 인증 정보입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| like | boolean | ✅ | 좋아요를 등록합니다. |

**Request**

```json
{
  "like": "좋아요 등록"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "nickname": "닉네임",
    "like": "좋아요 등록 여부",
    "like_count": "게시물 좋아요 수"
  }
}
```

**Error (400 Bad Request)**

```json
{
    "status": "error",
    "error": {
        "code": "BAD REQUEST",
        "message": "잘못된 요청입니다. 다시 확인하시고 사용해주세요.",
        "details": {}
    }
}
```

---

### 댓글 삭제

DELETE `/comments/{comment_id}`

작성했던 댓글을 삭제합니다. 삭제된 댓글은 복구할 수 없으므로 주의가 필요합니다. 삭제 성공 시 응답 본문 없이 204 상태 코드만 반환됩니다.

Path Parameter

| 파라미터       | 타입 | 필수 | 설명 |
|------------| --- | --- | --- |
| comment_id | integer | ✅ | 삭제할 댓글의 고유 식별자입니다. 해당 ID의 댓글이 존재해야 삭제가 수행됩니다. |

**Response (204 No Content)**

```json
{}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

---

### 댓글 수정

PATCH`/posts/{nickname}/comments/{comment_id}` 

본인이 기존에 작성한 댓글을 수정합니다. 전체 리소스를 교체하는 것이 아니라 요청 본문에 포함된 필드만 부분 업데이트 됩니다. 수정 시 `update_at` 필드가 자동으로 현재 시간으로 갱신됩니다.

Path Parameter

| 파라미터       | 타입 | 필수 | 설명 |
|------------| --- | --- | --- |
| comment_id | string | ✅ | 수정할 댓글의 고유 식별자입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | ✅ | 변경할 댓글 내용입니다. |

**Request**

```json
{
  "comment": "변경할 댓글 내용"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "comment_id": "0987654321",
    "nickname": "댓글 작성자",
    "comment": "변경된 댓글 내용",
    "comment_created_at": "2026-01-04T12:00:00Z",
    "comment_updated_at": "2026-01-06T12:00:00Z"
  }
}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

---

### 댓글 작성

POST `/posts/comments`

게시글에 새로운 댓글을 작성합니다. 댓글을 작성하려면 로그인이 필수적으로 이루어져야 합니다. 댓글 작성에 성공하면 자동으로 생성시간이 할당됩니다. 

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | 로그인 확인 위한 인증 정보입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ✅ | 댓글 작성자입니다. |
| comment_content | string | ✅ | 댓글 내용입니다. 댓글 내용은 최대 255자까지 작성할 수 있고 특수문자 사용이 가능합니다. |

**Request**

```json
{
  "nickname": "댓글 작성자",
  "comment_content": "댓글 내용"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "nickname": "댓글 작성자",
    "comment": "댓글 내용",
    "comment_id": "0987654321",
    "comment_created_at": "2026-01-04T12:00:00Z"
  }
}
```

---

### 게시글 삭제

DELETE `/posts/{post_id}`

본인이 작성한 기존 게시글을 삭제합니다. 삭제한 리소스는 복구할 수 없으므로 주의가 필요합니다. 삭제 성공 시 응답 본문 없이 204 상태 코드만 반환합니다.

Path Parameter

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | integer | ✅ | 삭제할 게시글의 고유 식별자입니다. 해당 ID의 리소스가 존재해야 삭제가 수행됩니다. |

**Response (204 No Content)**

```json
{}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

---

### 게시글 수정

**PATCH**`/users/{nickname}/posts/{post_id}`

본인이 작성한 기존 게시글을 수정합니다. 전체 게시글을 교체하는 것이 아니라 요청 본문에 포함된 필드만 부분 업데이트 됩니다. update_at 필드가 자동으로 현재 시간으로 갱신됩니다. 수정이 완료되면 자동으로 업데이트일이 갱신됩니다.

Path Parameters

| 파라미터    | 타입 | 필수 | 설명 |
|---------| --- | --- | --- |
| post_id | string | ✅ | 수정할 리소스의 고유 식별자입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | ❌ | 변경할 게시글 제목입니다. 생략 시 기존 값이 유지됩니다. |
| content | string | ❌ | 변경할 게시글 내용입니다. 생략 시 기존 값이 유지됩니다. |

Request

```json
{
  "post_title": "변경할 게시글 제목",
  "post_content": "변경할 게시글 내용"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "nickname": "닉네임",
    "title": "변경된 게시글 제목",
    "post": "변경된 게시글 내용",
    "post_created_at": "2026-01-04T12:00:00Z",
    "post_updated_at": "2026-01-06T12:00:00Z"
  }
}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

**Error (409 Conflict)**

```json
{
    "status": "error",
    "error": {
        "code": "CONFLICT",
        "message": "서버 현재 상태와 요청이 충돌했습니다.",
        "details": {}
    }
}
```

---

### 게시물 작성

**POST**`/posts`

새로운 게시물을 생성합니다. 생성에 성공하면 자동으로 고유 ID와 생성시간이 할당됩니다.입력할 수 있는 요소는 제목과 내용입니다. 요청 본문에 필수 필드인 `title`과 `content`가 할당됩니다. 게시물을 작성하면 자동으로 고유 아이디와 생성일이 할당됩니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer 토큰 형식의 인증정보입니다. 로그인 인증이 완료되어야 게시물을 작성할 수 있으므로 로그인 시 발급 받은 Access Token을 Bearer{token} 형식으로 전달합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | ✅ | 게시글의 제목입니다. 1자 이상 100자 이하의 문자열이어야 하며, 특수문자 사용이 가능합니다. |
| content | string | ✅ | 게시글의 내용입니다. 1자 이상 1000자 이하로 입력 가능하고 특수문자 사용이 가능합니다. |

**Request**

```json
{
  "title": "게시글 제목",
  "post": "게시글 내용"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "post_id": "124567890",
    "title": "새 게시글 제목",
    "post": "새 게시글 내용",
    "created_post_at": "2026-01-04T12:00:00Z"
  }
}
```

---

### 회원 탈퇴

DELETE`/users/{nickname}`

계정을 삭제합니다. 삭제된 계정은 복구할 수 없으므로 각별히 주의해야 합니다. 삭제 성공 시 응답 본문 없이 204 상태 코드만 반환됩니다.

Path Parameter

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ✅ | 삭제할 계정의 고유 식별자입니다. 해당 이메일이 존재해야 삭제할 수 있습니다. |

**Response (204 No Content)**

```json
{}
```

**Error (404 Not Found)**

```json
{
    "status": "error",
    "error": {
        "code": "NOT FOUND",
        "message": "요청한 리소스를 찾을 수 없습니다.",
        "details": {}
    }
}
```

---

---

### 회원가입

**POST** `/users`

새로운 계정을 생성합니다. 요청 본문에 필수 필드인 `email`, `password`, `nickname`을 포함해야 하며, 생성에 성공하면 자동으로 생성 시간이 할당됩니다.

**Request Body**

| 필드            | 타입 | 필수 | 설명 |
|---------------| --- | --- | --- |
| email         | string | ✅ | 계정의 고유 정보입니다. 유효한 이메일만 받을 수 있습니다. |
| password      | string | ✅ | 비밀번호는 8자 이상 16자 이하의 문자열이어야 하며 특수문자는 !, @, ^만 사용이 가능합니다. |
| nickname      | string | ✅ | 닉네임은 4자 이상 8자 이하의 문자열이어야 하며 특수문자 사용은 불가합니다. 다른 계정과 중복이 불가합니다. |
| profile_image | img, png | ❌ | 파일 형식은 반드시 img, png이어야 합니다. 미업로드 시 기본 프로필이 적용됩니다. |

**Request**

```json
{
  "email": "이메일",
  "password": "비밀번호",
  "nickname": "닉네임",
  "profile_image": "프로필 이미지"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "email": "이메일",
    "nickname": "닉네임",
    "profile_image": "프로필 이미지",
    "created_at": "2026-01-06T12:00:00Z"
  }
}
```

**Error (422 Validation Error)**

```json
{
    "status": "error",
    "error": {
        "code": "VALIDATION ERROR",
        "message": "유효성 검사에서 실패하였습니다. 처리할 수 없는 엔티티입니다.",
        "details": {}
    }
}
```

---

### 프로필 수정

PATCH`/users/{nickname}`

기존 닉네임, 프로필 이미지, 비밀번호를 수정할 수 있습니다. 전체 리소스를 교체하는 것이 아니라, 요청 본문에 포함된 필드만 부분 업데이트됩니다. 수정 시 `updated_at` 필드가 자동으로 현재 시간으로 갱신됩니다.

Path Parameter

| 파라미터     | 타입 | 필수 | 설명 |
|----------| --- | --- | --- |
| nickname | integer | ✅ | 사용자 계정의 고유 식별자입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ❌ | 변경할 닉네임입니다. 생략 시 기존 값이 유지됩니다. |
| profile_image | img, png | ❌ | 변경할 프로필 사진입니다. 생략 시 기존 값이 유지됩니다. |
| password | string | ❌ | 변경할 비밀번호입니다. 생략 시 기존 값이 유지됩니다. |

**Request**

```json
{
  "nickname": "변경할 닉네임",
  "profile_image": "변경할 프로필 사진",
  "password": "변경할 비밀번호"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "nickname": "변경된 닉네임",
      "profile_image": "변경된 프로필 사진",
    "updated_at": "2026-01-04T12:00:00Z"
  }
}
```

**Error (409 Conflict)**

```json
{
    "status": "error",
    "error": {
        "code": "CONFLICT",
        "message": "서버 현재 상태와 요청이 충돌했습니다.",
        "details": {}
    }
}
```

---

### 로그인

POST `/auth/token`

`email`과 `password`로 인증 절차를 거쳐 로그인합니다. 로그인에 성공하면 로그인 시간이 할당됩니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | 로그인을 확인을 위한 인증 정보입니다. |

**Request Body**

| 바디 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | ✅ | 로그인 하는데 필요한 고유 식별자입니다. |
| password | string | ✅ | 해당 계정을 생성할 때 설정한 알맞은 비밀번호를 입력해야 로그인에 성공합니다. |

**Request**

```json
{
  "email": "이메일",
  "password": "비밀번호"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
          "access_token": "q1w2e3r4...",
          "refresh_token": "q1w2e3r4...",
      "token_type": "Bearer",
      "expires_in": 3600,
      "sign_in_at": "2026-01-06T12:00:00Z"
    }
}
```

**Error (422 Validation Error)**

```json
{
  "status": "error",
  "data": {
      "code": "VALIDATION_ERROR",
      "message": "요청 데이터가 유효하지 않습니다.",
      "details": {
          "email": "유효한 이메일 형식이 아닙니다."
      }
    }
}
```

**Error (401 Unauthorized)**

```json
{
  "status": "error",
  "data": {
      "code": "UNAUTHORIZED",
      "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
      "details": {}
    }
}
```