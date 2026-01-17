# Cloud Community REST API Documentation

본 문서는 **Cloud Community** 프로젝트의 모든 API 명세를 담고 있다

### **내가 좋아요한 게시글 목록 조회**

**GET** `/users/me/likes`

로그인한 사용자가 **좋아요를 누른 게시글 목록**을 조회한다.

이 API는 **사용자 기준(User-centric) 조회**로 설계되며,좋아요 관계를 통해 연결된 게시글(Post) 정보를 목록 형태로 제공한다.

페이지네이션을 기본으로 제공한다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | number | X | 조회할 페이지 번호 (0부터 시작) |
| size | number | X | 페이지당 게시글 수 |

**Request Header**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 |
**Request Example**
```jsx
GET /users/me/likes?page=0&size=20
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "post_id": "post_123",
        "title": "REST API 설계 팁 정리",
        "author": {
          "id": "user_1",
          "nickname": "cloud_master"
        },
        "likes_count": 42,
        "liked_at": "2026-01-08T09:20:00Z"
      },
      {
        "post_id": "post_256",
        "title": "AWS 네트워크 기초 요약",
        "author": {
          "id": "user_4",
          "nickname": "vpc_guru"
        },
        "likes_count": 18,
        "liked_at": "2026-01-06T21:05:10Z"
      }
    ],
    "pagination": {
	    "page": 0,
	    "size": 20,
	    "total_elements": 2,
	    "total_pages": 1
    }
  }
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 인증 실패
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "인증이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

---

### 좋아요 상태 확인

**GET** `/posts/{post_id}/likes`

특정 게시글에 대해 **현재 로그인한 사용자의 좋아요 여부**와

해당 게시글의 **총 좋아요 수**를 함께 조회한다.

이 API는 **게시글 기준 좋아요 상태 조회**를 담당하며,

사용자 개인 상태(is_liked)와 집계 정보(likes_count)를 동시에 제공한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 좋아요 상태를 조회할 게시글 ID |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "post_id": "post_123",
    "is_liked": true,
    "likes_count": 42
  }
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 인증 실패
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "인증이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//404 Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

---

### **내가 쓴 댓글 목록 조회**

**GET** `/users/me/comments`

로그인한 사용자가 **본인이 작성한 댓글 목록**을 조회한다.

해당 API는 **인증된 사용자만 접근 가능**하며,

다른 사용자의 댓글은 조회할 수 없다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | number | X | 페이지 번호 (기본값: 0) |
| size | number | X | 페이지당 댓글 수 (기본값: 10) |
|  |  |  |  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "comments": [
      {
        "id": "comment_101",
        "post_id": "post_12",
        "content": "이 글 정말 도움이 됐어요!",
        "created_at": "2026-01-08T09:30:00Z"
      },
      {
        "id": "comment_102",
        "post_id": "post_15",
        "content": "동의합니다.",
        "created_at": "2026-01-08T10:05:00Z"
      }
    ],
    "pagination": {
      "page": 0,
      "size": 10,
      "total_items": 23,
      "total_pages": 3
    }
  }
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

---

### **댓글 목록 조회**

**GET** `/posts/{post_id}/comments`

특정 게시글에 등록된 **댓글** **목록** 을 조회한다.

댓글은 게시글(Post)에 종속되는 리소스이므로, 

댓글 목록 조회는 **게시글 하위 컬렉션** 으로 설계한다. 페이지네이션을 기본으로 제공한다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 댓글을 조회할 게시글 ID |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 | 기본값 |
| --- | --- | --- | --- | --- |
| page | number | X | 조회할 페이지 번호 (0부터 시작) | 0 |
| size | number | X | 페이지당 댓글 수 | 20 |

Request Examples

```jsx
GET /posts/post_123/comments?page=0&size=20
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "comment_501",
        "content": "정리 감사합니다! 이 부분이 특히 도움이 됐어요.",
        "author": {
          "id": "user_3",
          "nickname": "infra_dev"
        },
        "created_at": "2026-01-07T15:10:00Z",
        "updated_at": "2026-01-07T15:10:00Z"
      },
      {
        "id": "comment_502",
        "content": "혹시 페이징 기준이 0부터 시작하는 이유도 있나요?",
        "author": {
          "id": "user_8",
          "nickname": "backend_newbie"
        },
        "created_at": "2026-01-07T15:12:30Z",
        "updated_at": "2026-01-07T15:12:30Z"
      }
    ],
    "pagination":{
	    "page": 0,
	    "size": 20,
	    "total_elements": 2,
	    "total_pages": 1
	   }
  }
}
```

**Error Response Examples**

```jsx
//404 Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

```jsx
//400 Bad Request — 페이지 파라미터 오류
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "page와 size는 0 이상의 숫자여야 합니다.",
    "details": {
      "parameters": ["page", "size"]
    }
  }
}
```

---

### 내가 쓴 게시물 목록 조회

**GET** `/users/me/posts`

로그인한 사용자가 **직접 작성한 게시글 목록**만 조회한다.

해당 API는 인증이 필요하며,

**사용자 식별은 인증 토큰을 통해 서버에서 자동 처리**된다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 | 기본값 |
| --- | --- | --- | --- | --- |
| page | number | X | 조회할 페이지 번호 (0부터 시작) | 0 |
| size | number | X | 페이지당 게시글 수 | 10 |

Request Examples

```jsx
GET /users/me/posts?page=0&size=10
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "post_601",
        "title": "내가 작성한 첫 게시글",
        "views": 34,
        "likes_count": 2,
        "created_at": "2026-01-06T11:20:00Z"
      },
      {
        "id": "post_602",
        "title": "REST API 설계 후기",
        "views": 18,
        "likes_count": 1,
        "created_at": "2026-01-05T16:45:00Z"
      }
    ],
    "pagination": {
	    "page": 0,
	    "size": 10,
	    "total_elements": 2,
	    "total_pages": 1
	  }
  }
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

---

### 게시글 상세 조회

**GET** `/posts/{post_id}`

특정 게시글의 **상세 정보**를 조회한다.

게시글을 단건 조회할 때마다 **조회수(views)는 자동으로 증가**한다.

이 증가 동작은 클라이언트 요청에 의한 것이 아니라**서버 내부 로직의 부수 효과**다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 조회할 게시글 ID |

Request Examples

```jsx
GET /posts/post_123
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": "post123",
    "title": "첫 번째 게시글",
    "content": "게시글 본문 내용입니다.",
    "author": {
      "id": "user_1",
      "nickname": "cloud_jay"
    },
    "views": 153,
    "likes_count": 10,
    "created_at": "2026-01-07T10:00:00Z",
    "updated_at": "2026-01-07T10:30:00Z"
  }
}
```

**Error Response Examples**

```jsx
//404 Not Found — 존재하지 않는 게시글
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

---

### 게시글 정렬

**GET** `/posts`

게시글 목록을 **정렬 기준**에 따라 조회한다. 

정렬 기능은 별도의 엔드포인트를 만들지 않고,

**게시글 목록 조회 API에 Query Parameter로 확장** 하여 제공한다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **sort** | string | X | 정렬 기준 |
| page | number | X | 조회할 페이지 번호 (0부터 시작) |
| size | number | X | 페이지당 게시글 수 |

Request Examples

```jsx
GET /posts?sort=likes&page=0&size=10
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "post_301",
        "title": "인기 많은 게시글",
        "author": {
          "id": "user_7",
          "nickname": "hot_writer"
        },
        "views": 420,
        "likes_count": 58,
        "created_at": "2026-01-05T21:10:00Z"
      }
    ],
    "pagination": {
	    "page": 0,
	    "size": 10,
	    "total_elements": 1,
	    "total_pages": 1
	  }
  }
}
```

**Error Response Examples**

```jsx
//400 Bad Request — 정렬 파라미터 오류
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "sort 값은 latest, views, likes 중 하나여야 합니다.",
    "details": {
      "field": "sort"
    }
  }
}

```

---

### **게시글 검색**

**GET** `/posts`

게시글의 **제목 또는 내용** 을 기준으로 검색한다.

검색 기능은 별도의 엔드포인트를 만들지 않고,

**게시글 목록 조회 API에 Query Parameter로 확장**하여 제공한다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| search | string | X | 검색 키워드 (제목/내용 대상) |
| page | number | X | 조회할 페이지 번호 (0부터 시작) |
| size | number | X | 페이지당 게시글 수 |

Request Examples

```jsx
GET /posts?search=클라우드&page=0&size=10
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "post_201",
        "title": "클라우드 아키텍처 정리",
        "author": {
          "id": "user_3",
          "nickname": "infra_dev"
        },
        "views": 87,
        "likes_count": 6,
        "created_at": "2026-01-06T18:20:00Z"
      }
    ],
    "page": 0,
    "size": 10,
    "total_elements": 1,
    "total_pages": 1
  }
}
```

**Error Response Examples**

```jsx
//400 Bad Request — 검색 파라미터 오류
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "search 파라미터는 1자 이상이어야 합니다.",
    "details": {
      "field": "search"
    }
  }
}
```

---

### **게시글 목록 조회**

**GET** `/posts`

커뮤니티에 등록된 **전체 게시글 목록**을 조회한다.

페이지네이션을 기본으로 제공하며,

검색 및 정렬 조건은 **Query Parameter**로 확장 가능하다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | number | X | 조회할 페이지 번호 (0부터 시작) |
| size |  number | X | 페이지당 게시글 수 |

Request Examples

```jsx
GET /posts?page=0&size=10
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "id": "post_123",
        "title": "첫 번째 게시글",
        "author": {
          "id": "user_1",
          "nickname": "cloud_jay"
        },
        "views": 152,
        "likes_count": 10,
        "created_at": "2026-01-07T10:00:00Z"
      },
      {
        "id": "post_124",
        "title": "두 번째 게시글",
        "author": {
          "id": "user_2",
          "nickname": "sky_dev"
        },
        "views": 98,
        "likes_count": 3,
        "created_at": "2026-01-07T09:30:00Z"
      }
    ],
    "page": 0,
    "size": 10,
    "total_elements": 42,
    "total_pages": 5
  }
}
```

**Error Response Examples**

```jsx
//400 Bad Request — 페이지 파라미터 오류
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "page와 size는 0 이상의 숫자여야 합니다.",
    "details": {
      "parameters": ["page", "size"]
    }
  }
}
```

---

### **특정 회원 공개 프로필 조회**

**GET** `/users/{user_id}`

“다른 회원 조회”는 공개 프로필만 제공해야 한다. 즉, email 같은 민감 정보는 제외하고, 닉네임/프로필 이미지 정도만 반환한다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| user_id | string | O | 조회할 사용자 ID |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": "user_123",
    "nickname": "cloud_jay",
    "profile_image_url": "https://cdn.example.com/profile/2.png"
  }
}
```

**Error Response Examples**

```jsx
//404 Not Found — 존재하지 않는 사용자
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 사용자입니다.",
    "details": {
      "resource": "user",
      "user_id": "user_999"
    }
  }

```

---

### **내 프로필 조회**

**GET** `/users/me`

로그인한 사용자 본인의 정보를 조회한다. 

“내 프로필”은 로그인한 사용자만 접근 가능하다. 따라서 /users/me로 통일해 **“인증 필요 엔드포인트”**임을 URL에서 드러낸다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O  | Bearer 토큰 |

**Response (200 OK)**

```json
{
"status": "success",
"data": {
	"id": "user_123",
	"email": "[user@example.com](mailto:user@example.com)",
	"nickname": "cloud_jay",
	"profile_image_url": "https://cdn.example.com/profile/1.png",
	"created_at": "2026-01-07T12:00:00Z"
	}
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 토큰 없음 / 만료 / 위조
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "인증이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

---

### **좋아요 취소**

DELETE `/posts/{post_id}/likes`

특정 게시글에 대해 **이미 등록한 좋아요를 취소**한다.

좋아요 취소는 **로그인한 사용자만 가능**하며,

**본인이 눌렀던 좋아요만 취소**할 수 있다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 좋아요를 취소할 게시글 ID |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Request Example** 

```jsx
DELETE /posts/post_123/likes
```

**Response (204 NO Content)**

```json
// body 없음
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//404 Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

```jsx
//409 Conflict — 좋아요 미등록 상태
{
  "status": "error",
  "error": {
    "code": "CONFLICT",
    "message": "취소할 좋아요가 존재하지 않습니다.",
    "details": {
      "resource": "like",
      "post_id": "post_123"
    }
  }
}
```

---

### 좋아요 등록

POST `/posts/{post_id}/likes`

특정 게시글에 **좋아요를 등록**한다.

좋아요는 게시글(Post)에 대한 **사용자와 게시글 간의 관계**를 의미하며, **로그인한 사용자만** 좋아요를 누를 수 있다.

동일한 사용자는 하나의 게시글에 **중복 좋아요를 등록할 수 없다.**

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 좋아요를 등록할 게시글 ID |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Request Example** 

```jsx
POST /posts/post_123/likes
```

**Response (200 OK)**

```json
//본 API는 중복 요청에 대해 멱등성을 보장한다. 
//이미 좋아요를 누른 상태에서 동일한 요청이 다시 올 경우, 
//에러를 반환하는 대신 기존 정보를 바탕으로 성공 응답을 반환한다.
{
  "status": "success",
  "data": {
    "post_id": "post_123",
    "liked": true,
    "liked_at": "2026-01-08T12:40:00Z"
}
  
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//404 Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

```jsx
//409 Conflict — 이미 좋아요 등록됨
{
  "status": "error",
  "error": {
    "code": "ALREADY_LIKED",
    "message": "이미 좋아요를 누른 게시글입니다.",
    "details": {
      "resource": "like",
      "post_id": "post_123"
    }
  }
}
```

---

### 댓글 삭제

DELETE `/comments/{comment_id}`

본인이 작성한 **댓글을 삭제**한다.

댓글 삭제는 **로그인한 사용자만 가능**하며,

**댓글 작성자 본인만 삭제 권한**을 가진다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment_id | string | O | 삭제할 댓글 ID |

**Request Headers**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Response (204 No Content)**

```json
// body 없음
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//403 Forbidden — 삭제 권한 없음
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "본인이 작성한 댓글만 삭제할 수 있습니다.",
    "details": {
      "resource": "comment",
      "comment_id": "comment_101"
    }
  }
}

```

```jsx
//404 Not Found — 댓글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 댓글입니다.",
    "details": {
      "resource": "comment",
      "comment_id": "comment_999"
    }
  }
}

```

---

### 댓글 수정

PATCH `/comments/{comment_id}`

본인이 작성한 **댓글 내용을 수정**한다. 

댓글 수정은 **로그인한 사용자만 가능**하며, **댓글 작성자 본인만 수정 권한**을 가진다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment_id | string | O | 수정할 댓글 ID |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | string | O | 수정할 댓글 내용 |

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
    "id": "comment_101",
    "content": "수정된 댓글 내용입니다.",
    "updated_at": "2026-01-08T11:20:00Z"
  }
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//403 Forbidden — 수정 권한 없음
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "본인이 작성한 댓글만 수정할 수 있습니다.",
    "details": {
      "resource": "comment",
      "comment_id": "comment_101"
    }
  }
}
```

```jsx
//404 Not Found — 댓글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 댓글입니다.",
    "details": {
      "resource": "comment",
      "comment_id": "comment_999"
    }
  }
}
```

```jsx
//422 Validation Error — 댓글 내용 유효성 실패
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "content는 1자 이상이어야 합니다.",
    "details": {
      "field": "content"
    }
  }
}
```

---

### 댓글 작성

POST `/posts/{post_id}/comments`

특정 게시글에 **새로운 댓글을 작성**한다.

댓글 작성은 **로그인한 사용자만 가능**하며,

**작성자는 인증 토큰을 통해 서버에서 자동으로 식별**된다.

Path Parameters

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 댓글을 작성할 게시글 ID |

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer Access Token |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content | string | O | 댓글 내용 |

**Request Example** 

```json
{
  "content": "이 글 정말 도움이 많이 됐어요!"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": "comment_101",
    "post_id": "post_123",
    "content": "이 글 정말 도움이 많이 됐어요!",
    "author": {
      "id": "user_5",
      "nickname": "cloud_jay"
    },
    "created_at": "2026-01-08T10:30:00Z"
  }
}
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//404 Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

```jsx
//422 Validation Error — 댓글 내용 유효성 실패
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "content는 1자 이상이어야 합니다.",
    "details": {
      "field": "content"
    }
  }
}

```

---

### 게시글 삭제

DELETE `/posts/{post_id}`

특정 **게시글을 삭제**한다.

게시글 삭제는 로그인한 사용자만 가능하며, **본인이 작성한 게시글만 삭제할 수 있다.**

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string  | O | Bearer Access Token |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 삭제할 게시글 ID |

**Request Example** 

```jsx
DELETE /posts/post_401
```

**Response (204 NO Content)**

```json
// body 없음
```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//403 Forbidden — 삭제 권한 없음
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "게시글 삭제 권한이 없습니다.",
    "details": {
      "post_id": "post_401"
    }
  }
}
```

```jsx
//404  Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "post_id": "post_999"
    }
  }
}
```

---

### 게시글 수정

PATCH `/posts/{post_id}`

기존 **게시글을 수정**한다.

게시글 수정은 **로그인한 사용자**만 가능하며,

**해당 게시글의 작성자 본인만 수정**할 수 있다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string  | O | Bearer Access Token |
| Content-Type | string | O | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | string | O | 수정할 게시글 ID |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | X | 수정할 게시글 제목 (보내지 않으면 기존 값 유지) |
| content | string | X | 수정할 게시글 본문 (보내지 않으면 기존 값 유지) |

**Request Example** 

```json
{
  "title": "REST API 설계 정리 (수정)",
  "content": "게시글 수정 API에 대한 내용을 보완했습니다."
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": "post_401",
    "title": "REST API 설계 정리 (수정)",
    "content": "게시글 수정 API에 대한 내용을 보완했습니다.",
    "author": {
      "id": "user_5",
      "nickname": "cloud_jay"
    },
    "updated_at": "2026-01-07T15:10:00Z"
  }
}
```

**Error Response Examples**

```jsx
//400 Bad Request — 수정 필드 오류
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "수정할 필드가 없습니다.",
    "details": {
      "allowed_fields": ["title", "content"]
    }
  }
}
```

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//403 Forbidden — 작성자 아님
{
  "status": "error",
  "error": {
    "code": "FORBIDDEN",
    "message": "게시글 수정 권한이 없습니다.",
    "details": {
      "reason": "NOT_POST_OWNER"
    }
  }
}
```

```jsx
//404 Not Found — 게시글 없음
{
  "status": "error",
  "error": {
    "code": "NOT_FOUND",
    "message": "존재하지 않는 게시글입니다.",
    "details": {
      "resource": "post",
      "post_id": "post_999"
    }
  }
}
```

---

### 게시글 작성

POST `/posts`

새로운 **게시글을 작성**한다.

게시글 작성은 로그인한 사용자만 가능하며, **작성자는 인증 토큰을 통해 서버에서 자동으로 식별**된다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string  | O | Bearer Access Token |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string  | O | 게시글 제목 |
| content | string | O | 게시글 본문 내용 |

**Request Example** 

```json
{
  "title": "REST API 설계 정리",
  "content": "이번 글에서는 REST API Docs 작성 방법을 정리해봅니다."
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": "post_401",
    "title": "REST API 설계 정리",
    "content": "이번 글에서는 REST API Docs 작성 방법을 정리해봅니다.",
    "author": {
      "id": "user_5",
      "nickname": "cloud_jay"
    },
    "views": 0,
    "likes_count": 0,
    "created_at": "2026-01-07T14:00:00Z"
  }
}

```

**Error Response Examples**

```jsx
//401 Unauthorized — 로그인 필요
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다.",
    "details": {
      "reason": "MISSING_OR_INVALID_TOKEN"
    }
  }
}
```

```jsx
//422 Validation Error — 제목/내용 유효성 실패
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "title은 1자 이상이어야 합니다.",
    "details": {
      "field": "title"
    }
  }
}
```

---

### 회원 탈퇴

DELETE `/users/me`

로그인한 사용자 계정을 삭제한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 |

**Response (204 No Content)**

```json
// body 없음
```

**Error Response Examples**

```jsx
//401 Unauthorized — 토큰 없음 / 만료 / 위조
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "인증이 필요합니다.",
    "details": {
      "reason": "INVALID_OR_EXPIRED_TOKEN"
    }
  }
}
```

---

### **내 프로필 수정**

PATCH `/users/me`

닉네임, 프로필 이미지, 비밀번호를 부분 수정한다. (변경할 필드만 전달)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | O | Bearer 토큰 |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | X | 변경할 닉네임 |
| profile_image_url | string(URL) | X | 변경할 프로필 이미지 URL |
| password | string | X | 변경할 비밀번호 |

**Request Example** 

```json
{
  "nickname": "cloud_jay",
  "profile_image_url": "https://cdn.example.com/profile/2.png"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": "user_123",
    "email": "user@example.com",
    "nickname": "cloud_jay",
    "profile_image_url": "https://cdn.example.com/profile/2.png",
    "updated_at": "2026-01-07T12:10:00Z"
  }
}
```

**Error Response Examples**

```jsx
//400 Bad Request — 수정할 필드가 없음
{
  "status": "error",
  "error": {
    "code": "INVALID_REQUEST",
    "message": "수정할 필드가 없습니다.",
    "details": {
      "allowed_fields": ["nickname", "password", "profile_image_url"]
    }
  }
}
```

```jsx
//401 Unauthorized — 토큰 없음 / 만료 / 위조
{
  "status": "error",
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "인증이 필요합니다.",
    "details": {
      "reason": "INVALID_OR_EXPIRED_TOKEN"
    }
  }
}
```

```jsx
//422 Validation Error — 닉네임/비밀번호 정책 위반
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "password는 8자 이상이며 특수문자를 포함해야 합니다.",
    "details": {
      "field": "password"
    }
  }
}
```

```jsx
//409 Conflict — 닉네임 중복
{
  "status": "error",
  "error": {
    "code": "DUPLICATE_RESOURCE",
    "message": "이미 사용 중인 닉네임입니다.",
    "details": {
      "field": "nickname"
    }
  }
}
```

---

### **로그인**

POST  `/sessions`

이메일/비밀번호로 인증 후 access token을 발급한다.

**Request Body**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 가입한 이메일 |
| password | string | O | 비밀번호 |

**Request Example** 

```json
{
  "email": "user@example.com",
  "password": "P@ssw0rd!"
}
```

**Response (200 OK)** 

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

**Error Response Examples**

```jsx
//401 Unauthorized — 이메일/비밀번호 불일치
{
  "status": "error",
  "error": {
    "code": "AUTHENTICATION_FAILED",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
    "details": {
      "reason": "INVALID_CREDENTIALS"
    }
  }
```

```jsx
//422 Validation Error — 입력값 형식 오류
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "email은 올바른 이메일 형식이어야 합니다.",
    "details": {
      "field": "email"
    }
  }
}
```

---

### 회원가입

POST `/users`

이메일/비밀번호/닉네임으로 계정을 생성한다. 프로필 이미지는 선택이다.

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 로그인 식별자(이메일) |
| password | string | O | 로그인 비밀번호 |
| nickname | string | O | 커뮤니티 표시 이름 |
| profile_image_url | string | X | 프로필 이미지 URL |

**Request Example** 

```json
{
  "email": "user@example.com",
  "password": "P@ssw0rd!",
  "nickname": "cloud_jay",
  "profile_image_url": "https://cdn.example.com/profile/1.png"
}

```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": "user_123",
    "email": "user@example.com",
    "nickname": "cloud_jay",
    "profile_image_url": "https://cdn.example.com/profile/1.png",
    "created_at": "2026-01-07T12:00:00Z"
  }
}
```

**Error Response Examples**

```jsx
//409 Conflict — 이메일 중복
{
  "status": "error",
  "error": {
    "code": "DUPLICATE_RESOURCE",
    "message": "이미 사용 중인 이메일입니다.",
    "details": {
      "field": "email"
    }
  }
}
```

```jsx
//422 Validation Error — 입력값 형식 오류
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "nickname은 2자 이상이어야 합니다.",
    "details": {
      "field": "nickname"
    }
  }
}
```

---