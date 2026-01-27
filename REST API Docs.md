# REST API Docs

### { 좋아요 상태 확인 }

**GET** `/users/me/posts/likes/summary` 

현재 사용자가 게시글에서 받은 좋아요의 여부 및 총 좋아요 수, 총 게시글 수 를 조회합니다

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| from | string | ❌ | date-time/ 집계 시작 시간 |
| to | string | ❌ | date-time/집계 종료 시간 |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": 
    {
      "has_any_like": true,
      "total_like_count": 182 ,
      "post_count": 12
    }
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "로그인이 필요한 기능입니다."
	}
}
```

**Response (500 Internal Server Error)**

```json
{
	"status": "error",
	"error": {
	  "code": "INTERNAL SERVER ERROR",
	  "message": "서버 내부 오류입니다."
	}
}
```

---

### { 내가 좋아요한 게시글 목록 }

**GET** `/users/me/likes` 

현재 사용자가 좋아요를 누른 게시글을 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | int | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준, 조회수 기준으로 지정할 수 있음, 기본값 : 생성일 기준) |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
	  "content":[
		  {
	      "id": "like_1",
	      "like_at": "2026-01-04T12:00:00Z",
		    "target": {  
		      "comment": "첫번째 게시글",
		      "author": "홍길동",
			    "like_count": 4,
			    "created_at": "2026-01-04T12:00:00Z"
			   }
	    },
	   {
	      "id": "like_2",
	      "like_at": "2026-01-04T12:00:00Z",
		    "target": {  
		      "comment": "두번째 게시글",
		      "author": "고길동",
			    "like_count": 2,
			    "created_at": "2026-01-04T12:00:00Z"
			   }
	    }
   ],
  "pagination": {
    "page": 1,
    "size": 10,
    "sort": "created_at",
    "order": "desc",
    "totalElements": 2
  }
 }
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "권한이 없습니다."
	}
}
```

---

### { 내가 쓴 댓글 목록 }

**GET** `/users/me/comments` 

로그인된 사용자가 작성한 댓글 목록을 불러옵니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | int | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준, 조회수 기준으로 지정할 수 있음, 기본값 : 생성일 기준) |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
	  "content":[
		  {
	      "id": "comment_1",
	      "content": "첫번째 댓글",
	      "author": "홍길동",
		    "like_count": 4,
		    "created_at": "2026-01-04T12:00:00Z"
	    },
	    {
	      "id": "comment_2",
	      "content": "두번째 댓글",
	      "author": "고길동",
		    "like_count": 7,
		    "created_at": "2026-01-04T12:01:00Z"
		  }
   ],
  "pagination": {
    "page": 1,
    "size": 10,
    "sort": "created_at",
    "order": "desc",
    "totalElements": 2
  }
 }
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "권한이 없습니다."
	}
}
```

---

### { 댓글 목록 조회}

**GET** `/posts/{postId}/comments`

특정 게시글의 댓글 목록을 조회합니다

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **postId** | string | ✅ | 조회할 게시글의 고유 식별자 입니다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | int | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준, 조회수 기준으로 지정할 수 있음, 기본값 : 생성일 기준) |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
	  "content":[
		  {
	      "id": "comment_1",
	      "comment": "첫번째 댓글",
	      "author": "홍길동"
		    "like_count": 4,
		    "created_at": "2026-01-04T12:00:00Z"
	    },
	    {
	      "id": "comment_2",
	      "content": "두번째 댓글",
	      "author": "고길동"
		    "like_count": 7,
		    "created_at": "2026-01-04T12:01:00Z"
		  }
   ],
  "pagination": {
    "page": 1,
    "size": 10,
    "sort": "created_at",
    "order": "desc",
    "totalElements": 2
  }
 }
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 내가 쓴 게시글 목록 }

**GET** `/users/me/posts` 

현재 로그인한 계정으로 작성한 게시글 목록을 불러옵니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | int | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준, 조회수 기준으로 지정할 수 있음, 기본값 : 생성일 기준) |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": "post_1",
      "title": "첫번째 포스트",
      "author": "홍길동",
      "created_at": "2026-01-04T12:00:00Z"
    },
    {
      "id": "post_2",
      "title": "두번째 포스트",
      "author": "김철수",
      "created_at": "2025-04-04T11:00:00Z"
    },
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "sort": "created_at",
    "order": "desc"
  }
}
```

---

### { 게시글 정렬 }

**GET** `/posts` 

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | int | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | int | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준, 조회수 기준으로 지정할 수 있음, 기본값 : 생성일 기준) |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": "post_1",
      "title": "첫번째 포스트",
      "author": "홍길동",
      "created_at": "2026-01-04T12:00:00Z"
    },
    {
      "id": "post_2",
      "title": "두번째 포스트",
      "author": "김철수",
      "created_at": "2025-04-04T11:00:00Z"
    },
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "sort": "like_count",
    "order": "desc"
  }
}
```

---

### { 게시글 검색 }

**GET** `/posts` 

제목, 내용을 키워드로 게시글을 검색합니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| keyword | stirng | ❌ | 검색 키워드(제목/내용) |
| page | int | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | int | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준으로 지정할 수 있음 |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
    {
      "id": "post1",
      "name": "첫번째 포스트",
      "title": "안녕하세요"
      "author": {
		    "id" : "user_123",
				"nickname" : "홍길동"
			}
      "view_count": 255,
      "like_count": 123,
      "dislike_count": 2,
      "created_at": "2026-01-04T12:00:00Z",
      "update_at": "2026-02-04T12:00:00Z"
    },
    {
      "id": "post3",
      "name": "세번째 포스트",
      "title": "안녕히 가세요"
      "author": {
		    "id" : "user_321",
				"nickname" : "동길홍"
			}
      "view_count": 213,
      "like_count": 98,
      "dislike_count": 6,
      "created_at": "2026-01-04T12:03:00Z",
      "update_at": "2026-02-04T12:50:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "size": 10,
    "sort": "like_count",
    "order": "desc"
  }
}
```

---

### { 게시글 상세 조회}

**GET** `/post/{postId}` 

특정 게시글을 상세 조회 합니다. 게시글의 전체 정보를 반환합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | string | ✅ | 조회할 게시글의 고유 식별자 입니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "id": "post_1",
      "title": "첫번째 포스트",
      "content": "첫번째 포스트에 대한 설명",
      "author": {
	      "id" : "user_123",
				"nickname" : "홍길동"
			},
      "view_count": 255,
      "like_count": 123,
      "dislike_count": 2,
      "created_at": "2026-01-04T12:00:00Z",
      "update_at": "2026-02-04T12:00:00Z"
    }
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 게시글 목록 조회 }

**GET** `/posts` 

게시글 목록을 눌렀을때 조회되는 전체 게시글 목록 조회입니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | number | ❌ | 페이지 번호입니다. (1부터 시작, 기본값 : 1) |
| size | number | ❌ | 페이지당 게시글 수 (최소 1부터 최대 20까지, 기본값 : 10) |
| sort | string | ❌ | 정렬 기준 필드입니다. 생성일 기준 또는 좋아요 기준으로 지정할 수 있으며, 기본값은 생성일 내림차순으로 정렬됩니다. |
| order | string | ❌ | 정렬 방향 (asc/desc 기본값 :desc) |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": [
	  {
      "id": "post_1",
      "title": "첫번째 포스트",
      "author": "홍길동",
      "created_at": "2026-01-04T12:00:00Z"
    },
    {
      "id": "post_2",
      "title": "두번째 포스트",
      "author": "김철수",
      "created_at": "2025-04-04T11:00:00Z"
    }
   ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "order": "desc"
  }
}
```

---

### { 특정 회원 조회 }

**GET** `/users/{userId}` 

특정 사용자의 공개된 프로필 정보를 조회한다.

로그인 여부와 관계없이 접근 가능하며, 공개된 정보만 반환한다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| userId | string | ✅ | 조회할 사용자 ID |

**Response (200 OK)**

```json
{
	"id": "res_123",
  "nickname": "테스트_1234",
	"profile_image_url": "https://example.com/profiles/res_123.png"
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
			"code": "USER_NOT_FOUND",
			"message": "사용자를 찾을 수 없습니다."
		}
}
```

---

### { 내 프로필 조회 }

**GET** `/users/me` 

로그인한 사용자의 본인 프로필 정보를 조회한다.

인증 토큰을 기반으로 사용자를 식별하며, 본인만 접근할 수 있다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Response (200 OK)**

```json

{
	"status": "success",
  "data": {
	  "id": "res_123",
	  "email": "test@admin.com",
	  "password": "!Testadmin1234",
	  "nickname": "테스트_1234",
		"created_at": "2026-01-04T12:00:00Z"
	}
}
```

**Response (401 Unauthorized)**

```json
{
	"code": "UNAUTHORIZED",
	"message": "인증이 필요합니다."
}
```

---

### { 좋아요 취소 }

DELETE `/posts/{postId}/likes`

특정 게시글에 눌렀던 좋아요를 취소합니다

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **postId** | string | ✅ | 좋아요를 누른 게시글의 고유 식별자 입니다. |

**Response (204 No Content)**

```json
**204 No Content**
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 좋아요 등록 }

**POST**`/posts/{postId}/likes` 

게시글에 좋아요를 등록합니다. 로그인이 필요한 기능입니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **postId** | string | ✅ | 좋아요를 누를 게시글의 고유 식별자 입니다. |

**Response (201 Create)**

```json
{
  "status": "success",
  "data": {
    "id": "like_123",
    "post_id": "post_1",
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "로그인이 필요한 기능입니다."
	}
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

**Response (409 Conflict)**

```json
{
  "status": "error",
  "error": {
    "code": "ALREADY_LIKED",
    "message": "이미 좋아요 누른 게시글입니다."
  }
}
```

---

### { 댓글 삭제 }

DELETE `/posts/{postId}/comments/{commentId}`

본인이 작성한 댓글을 삭제합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | string | ✅ | 댓글이 작성된 게시글의 고유 식별자 입니다. |
| commentId | string | ✅ | 작성된 댓글의 고유 식별자 입니다. |

**Response (204 No Content)**

```json
204 No Content
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "권한이 없습니다."
	}
}
```

**Response (403 Forbidden)**

```json
{
	"status": "error",
	"error": {
	  "code": "FORBIDDEN",
	  "message": "해당 댓글을 삭제할 권한이 없습니다."
	}
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 댓글 수정 }

**PATCH**`/posts/{postId}/comments/{commentId}`

새로운 리소스를 생성합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Content-Type | string | ✅ | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | string | ✅ | 댓글이 작성된 게시글의 고유 식별자 입니다. |
| commentId | string | ✅ | 작성된 댓글의 고유 식별자 입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | ✅ | 수정될 댓글 내용입니다 |

**Request Example**

```json
{
  "comment": "수정된 코멘트"
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": "comment_1",
    "comment": "수정된 코멘트",
    "created_at": "2026-01-04T12:00:00Z"
    "update_at": "2026-01-04T12:00:00Z"
  }
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 댓글 작성 }

**POST**`/posts/{postId}/comments`

새로운 리소스를 생성합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Content-Type | string | ✅ | application/json |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | string | ✅ | 댓글을 작성할 게시글의 고유 식별자 입니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | ✅ | 댓글 내용입니다 |

**Request Example**

```json
{
  "comment": "새 댓글"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": "comment_1",
    "comment": "새 댓글",
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 게시글 삭제 }

**DELETE** `/posts/{postId}`

자신이 작성한 게시글을 삭제합니다

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | string | ✅ | 수정할 게시글의 고유 식별자 입니다. |

**Response (204 No Content)**

```json
204 No Content
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "권한이 없습니다."
	}
}
```

**Response (403 Forbidden)**

```json
{
	"status": "error",
	"error": {
	  "code": "FORBIDDEN",
	  "message": "해당 게시글을 삭제할 권한이 없습니다."
	}
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 게시글 수정 }

**PATCH** `/posts/{postId}`

본인이 작성한 게시글을 수정합니다

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Content-Type | string | ✅ | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | ❌ | 게시글 제목 |
| content | string | ❌ | 게시글 내용 |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| postId | string | ✅ | 수정할 게시글의 고유 식별자 입니다. |

**Request Example**

```json
{
  "title": "수정된 타이틀",
  "content": "수정된 콘텐츠"
}
```

**Response (200 OK)**

```json
// Response (200 OK)
{
  "status": "success",
  "data": {
    "id": "post_1",
    "title": "수정된 타이틀",
    "content": "수정된 콘텐츠",
    "updated_at": "2026-01-04T13:00:00Z"
  }
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "권한이 없습니다."
	}
}
```

**Response (403 Forbidden)**

```json
{
	"status": "error",
	"error": {
	  "code": "FORBIDDEN",
	  "message": "해당 게시글을 수정할 권한이 없습니다."
	}
}
```

**Response (404 Not Found)**

```json
{
	"status": "error",
	"error": {
	  "code": "POST_NOT_FOUND",
	  "message": "게시글을 찾을 수 없습니다."
	}
}
```

---

### { 게시글 작성 }

**POST** `/posts`

새로운 게시글을 작성합니다. 로그인이 필요한 기능입니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Content-Type | string | ✅ | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | ✅ | 게시글 제목 |
| content | string | ✅ | 게시글 내용 |

**Request Example** 

```json
{
  "title": "새 포스트",
  "content": "새 포스트에 대한 설명"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": "post_1234",
    "title": "새 포스트",
    "content": "새 포스트에 대한 설명",
    "author": {
	      "id" : "user_123",
				"nickname" : "홍길동"
			},
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "로그인이 필요합니다."
	}
}
```

---

### { 회원 탈퇴 }

**DELETE** `/users/me`

로그인한 사용자 본인의 계정을 탈퇴(삭제)한다.

인증 토큰을 기반으로 사용자를 식별하며, 탈퇴 처리 후 해당 계정은 더 이상 사용할 수 없다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |

**Response (204 No Content)**

```json
No Content
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "인증이 필요합니다."
	}
}
```

---

### { 비밀번호 변경 }

PUT`/users/me/password`

로그인한 사용자의 비밀번호를 변경합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Content-Type | string | ✅ | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| current_password | string | ✅ | 기존 패스워드 |
| new_password | string | ✅ | 새로운 패스워드 |

**Request Example**

```json
{
  "current_password": "!Test1234",
  "new_password": "N!Test1234"
}
```

**Response (204 No Content)** 

```json
No Content
```

**Response (400 Bad Request)** 

```json
{
	"status": "error",
	"error": {
		"code": "INVALID_PASSWORD",
		"message" : "비밀번호는 8자 이상이며 특수문자, 알파벳 대문자, 숫자를 포함해야 합니다."
	}
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "인증이 필요합니다."
	}
}
```

---

### { 프로필 이미지 수정 }

**PUT**`/users/me/profile-image`

로그인한 사용자의 닉네임을 수정합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Context-Type | string | ✅ | multipart/form-data |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| profileImage | file | ✅ | 프로필 이미지파일 |

**Request Example** 

```json
profileImage:(binary file)
```

**Response (200 OK)**

```json
{
	"status": "success",
  "data": {
	  "profile_image_url": "https://cdn.example.com/profiles/res_124.png"
	}
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "인증이 필요합니다."
	}
}
```

---

### { 프로필 닉네임 수정 }

PATCH `/users/me`

로그인한 사용자의 닉네임을 수정합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Authorization | string | ✅ | Bearer {access_token} |
| Content-Type | string | ✅ | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| nickname | string | ✅ | 변경할 닉네임 |

**Request Example** 

```json
{
	"nickname": "새로운닉네임_12"
}
```

**Response (200 OK)**

```json
{
	"status": "success",
  "data": {
	  "id": "res_124",
	  "email": "test@admin.com",
	  "nickname": "새로운닉네임_12",
	  "profile_image_url": "https://cdn.example.com/profiles/res_124.png",
	  "created_at": "2026-01-04T12:00:00Z"
	}
}
```

**Response (400 Bad Request)**

```json
{
	"status": "error",
	"error": {
		"code": "INVALID_NICKNAME",
		"message": "닉네임 형식이 올바르지 않습니다."
	}
}
```

**Response (409 Conflict)**

```json
{
	"status": "error",
	"error": {
		"code": "DUPLICATE_NICKNAME",
		"message": "이미 사용중인 닉네임입니다."
	}
}
```

**Response (401 Unauthorized)**

```json
{
	"status": "error",
	"error": {
	  "code": "UNAUTHORIZED",
	  "message": "인증이 필요합니다."
	}
}
```

---

### { 로그인 }

**POST** `/auth/tokens`

이메일과 비밀번호로 사용자를 인증하고, 토큰을 발급한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | ✅ | application/json |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | ✅ | 회원가입시 입력한 이메일 주소 |
| password | string | ✅ | 회원가입시 입력한 패스워드 |

**Request Example**

```json
{
	"email": "test@admin.com",
  "password": "!Testadmin1234"
}
```

**Response (201 Created)** 

```json
{
	"status": "success",
  "data": {
		"access_token": "abcdefghIjKLNMoPQrsTUVwxYz",
		"token_type": "Bearer",
		"expires_in": "3600"
	}
}
```

**Response (400 Bad Request)** 

```json
{
	"status": "error",
	"error": {
		"code": "INVALID_REQUEST",
		"message": "요청값이 올바르지 않습니다."
	}
}
```

**Response (401 Unauthorized)** 

```json
{
	"status": "error",
	"error": {
		"code": "INVALID_CREDENTIALS",
		"message": "이메일 또는 비밀번호가 올바르지 않습니다."
	}
}
```

---

### { 회원가입 }

**POST**`/auth/signup`

새로운 회원을 생성합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| content-Type | string | ✅ | multipart/form-data |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |  |
| --- | --- | --- | --- | --- |
| email | string | ✅ | 회원가입시 아이디로 사용될 이메일 주소입니다.  |  |
| password | string | ✅ | 8자 이상, 특수문자 1개 이상, 알파벳 대문자1개 이상, 숫자 1개 이상 포함 필수 |  |
| nickname | string | ✅ | 2~20자, 한글/영문/숫자/언더스코어(_)만 허용, 공백 불가, 중복 불가 |  |
| profile | file | ❌ | 필수 X, 사용자 미입력시 기본이미지 적용 |  |

**Request Example** 

```json
{
  "email": "test@admin.com",
  "password": "!Test1234",
  "nickname": "테스트_1234"
}
```

**Response (201 Created)** 

```json
{
	"status": "success",
  "data": {
		"id": "res_124",
		"email" : "test@admin.com",
		"nickname": "테스트_1234",
		"created_at": "2026-01-04T12:00:00Z"
	}
}
```

**Response (400 Bad Request)** 

```json
{
	"status": "error",
	"error": {
		"code": "INVALID_PASSWORD",
		"message" : "비밀번호는 8자 이상이며 특수문자, 알파벳 대문자, 숫자를 포함해야 합니다."
	}
}
```

**Response (409 Conflict) - 이메일 중복**

```json
{
	"status": "error",
	"error": {
		"code": "DUPLICATE_EMAIL",
		"message" : "이미 사용중인 이메일입니다."
	}
}
```

**Response (409 Conflict) - 닉네임 중복**

```json
{
	"status": "error",
	"error": {
		"code": "DUPLICATE_NICKNAME",
		"message" : "이미 사용중인 닉네임입니다."
	}
}
```

---