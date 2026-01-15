# 클라우드 커뮤니티 REST API Docs

<aside>
<img src="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" alt="notion://custom_emoji/845a6cfa-ad4b-4505-8350-960c9f51a87a/168954da-c755-8023-8dcf-007afaa4b2e6" width="40px" />

전체화면으로 해놓고 구현하시면 편합니다!
Cmd + T (Ctrl + T) 누르면 탭 추가가 가능합니다. 참고하세요!

창 추가하는건 Cmd + Shift + N (Ctrl + Shift + N) 입니다!.

</aside>

### { 내가 좋아요한 게시글 목록 조회 }

**GET** `/users/me/likes/liked_posts` 

로그인한 사용자가 좋아요를 등록한 게시글 목록을 조회하기 위한 리소스이다.  사용자 기준으로 좋아요 관계가 있는 게시글들을 리스트 형태로 반환한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 사용자가 좋아요를 누른 게시글 목록을 조회해야 하기 때문에 Bearer 토큰 인증이 필요합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
	  "list": [
    {
      "id": 1,
      "title": "지금은 6시 8분",
      "created_at": "2026-01-04T12:00:00Z"
    },
    {
	    "id": 3,
	    "title": "지금은 6시 9분",
	    "created_at": "2026-01-05T12:00:00Z"
	  }
  ]
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 좋아요 상태 확인 }

**GET** `/posts/{post_id}/likes` 

게시글의 좋아요 상태를 조회하는 리소스입니다. 해당 정보는 좋아요 등록/취소 API의 response에도 포함되어 있으나, 과제 요구사항에 따라 별도로 정의하였습니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 사용자가 좋아요를 누른 게시글 목록을 조회해야 하기 때문에 Bearer 토큰 인증이 필요합니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | integer | O | 해당 게시글의 좋아요 상태를 조회해야 하기 때문에 postId 값을 이용한다. |

**Response (200 OK)**

```json
{
  "liked": true
  "like_count": 22
}
```

---

### { 내가 쓴 댓글 목록 }

**GET** `/users/me/comments` 

로그인 한 사용자의 댓글만 조회하여 목록을 보여주는 리소스이다. (어떤 게시글인지 상관없기때문에 posts/{post_id} 로 안함)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 로그인 한 사용자의 댓글만 조회하여 목록을 보여주어야 하기 때문에 Bearer 토큰 인증이 필요하다. |

본 API는 로그인 사용자(`me`) 기준의 리소스를 조회하므로 별도의 Path Parameter를 사용하지 않는다

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
	  "list": [
    {
      "id": 1,
      "comment": "정말 웃겨요.",
      "created_at": "2026-01-04T12:00:00Z"
    },
    {
	    "id": 2,
	    "comment": "정말 재밌어요.",
	    "created_at": "2026-01-05T12:00:00Z"
	  }
  ]
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 댓글 목록 조회 }

**GET** `/posts/{post_id}/comments` 

특정 게시글의 댓글 목록을 조회하는 리소스입니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| post_id | integer | O | 특정 게시물의 댓글 목록을 조회하기 위해서 postId값을 이용한다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
	  "list": [
    {
      "nickname": "욱정선",
      "comment": "너무 공감되네요",
      "created_at": "2026-01-04T12:00:00Z"
    },
    {
	    "nickname": "제프",
	    "comment": "열심히 합시다",
	    "created_at": "2026-01-05T12:00:00Z"
	  }
  ]
 }
}
```

---

### { 내가 쓴 게시글 목록}

**GET** `/users/me/posts` 

로그인한 사용자가 쓴 게시글을 조회하여 목록을 보여주는 리소스이다.(로그인 인증)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 로그인 한 사용자가 쓴 게시글을 조회하는 리소스이므로 Bearer 토큰 인증이 필요합니다. |

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| user_id | integer | O | 로그인 한 사용자의 Id값을 통해 자신이 쓴 게시글을 조회한다. |

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 나중에 데이터 양이 많아졌을때 정렬이 힘드므로 범위를 지정하기 위해 포함하였습니다. |
| limit | integer | X | 한 페이지에 포함될 리소스의 개수를 제한하였습니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "list": [
      {
        "id": 4,
        "title": "선정욱이 쓴거임",
        "created_at": "2026-01-04T12:00:00Z"
      },
      {
        "id": 5,
        "title": "선정욱이 쓴거임2",
        "created_at": "2026-01-05T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 게시글 상세 조회 }

**GET** `/posts/{post_id}` 

게시글의 id값을 통해 게시글을 상세 조회합니다.

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| id | integer | O | 게시글 id값을 통해 게시글을 상세조회합니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 2,
    "title": "1월 7일의 비밀",
    "content": "1월 7일은 너무 춥고 배고픈 날이다",
    "author": {
      "id": 5,
      "nickname": "욱정선"
    },
    "created_at": "2026-01-07T12:00:00Z"
  }
}
```

Response (404 Not Found)

```json
{
  "status": "fail",
  "message": "해당 게시글을 찾을 수 없습니다."
}
```

---

### { 게시물 정렬 }

**GET** `/posts` 

게시물을 최신순, 조회수순, 좋아요순 등으로 정렬합니다. page와 limit 파라미터를 활용하여 원하는 범위의 데이터만 정렬 가능합니다.

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| sort | integer | X | 최신순, 조회수순, 좋아요순 으로 정렬하기 위해서 sort를 사용하여 정렬할 수 있도록 하였습니다. |
| page | integer | X | 나중에 데이터 양이 많아졌을때 정렬이 힘드므로 범위를 지정하기 위해 포함하였습니다. |
| limit | integer | X | 한 페이지에 포함될 리소스의 개수를 제한하였습니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
		"list" : [
    {
      "id": 3,
      "title": "JEFF의 파이썬 강의",
      "created_at": "2026-01-06T15:00:00Z"
    },
    {
	    "id": 10,
	    "title": "코딩은 왜이렇게 어려운가",
	    "created_at": "2026-01-05T12:00:00Z"
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

### { 게시글 검색 }

**GET** `/posts` 

keyword를 통해 전체 게시판에서 keyword를 포함한 제목과 내용을 검색합니다. 

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| keyword | integer | X | 제목/내용에 keyword가 포함되어 있다면 검색이 되도록 합니다. |
| page | integer | X | 게시글은 계속 늘어나기 때문에 나중에 양이 방대해질 수도 있으므로 범위를 지정하기 위해 포함했습니다. |
| limit | integer | X | 한 페이지에 포함될 리소스의 개수도 제한하는 것을 더 효율적이기 때문에 포함했습니다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "AWS는 왜 위대한가",
        "content": "AWS는 혁신적인 클라우드..."
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }
}

```

---

### { 게시글 목록 조회 }

**GET** `/posts` 

게시글 목록을 조회합니다.(페이지네이션 적용)

**Query Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| page | integer | X | 조회할 페이지 번호입니다. 범위를 지정하지 않으면 1페이지만 출력됩니다. |
| limit | integer | X | 한 페이지에 포함될 리소스 개수입니다. |
| sort | string | X | 결과 정렬 기준 필드입니다.  |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "AWS는 왜 위대한가",
        "author": {
          "id": 3,
          "nickname": "선정욱"
        },
        "created_at": "2026-01-04T12:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100
    }
  }
}

```

---

### { 특정 회원 조회 }

**GET** `/users/{user_id}` 

특정 회원 조회: 다른 사용자의 공개 프로필 조회

**Path Parameters**

| 파라미터 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| id | integer | O | 사용자 고유 식별자인 id값을 이용해서 특정 회원을 조회한다. |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "id": 1,
      "nickname": "욱정선",
      "profile_image" : "https://newimage.com/images/profile.png",
      "created_at": "2026-01-04T12:00:00Z"
  }
}
```

Response (404 Not Found)

```json
{
  "status": "fail",
  "message": "해당 유저를 찾을 수 없습니다."
}
```

---

### { 내 프로필 조회 }

**GET** `/users/me` 

로그인한 사용자 본인 정보를 조회합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | Bearer 토큰 인증 |

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
      "id": "seonjeongug2@gmail.com",
      "nickname": "정정욱",
      "profile_image": "https://example.com/images/profile.png",
      "created_at": "2026-01-04T12:00:00Z"
    }
}
```

---

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

### { 좋아요 취소 }

**DELETE** `/posts/{post_id}/likes`

로그인한 사용자가 특정 게시글에 대해 등록한 좋아요를 취소하기 위한 리소스이다. 인증된 사용자 본인이 생성한 좋아요 리소스만 삭제할 수 있다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 로그인 한 사용자가 자기가 누른 좋아요를 취소해야 하므로 Bearer 토큰 인증이 필요합니다. |

**Response (200 OK)** 

```json
{
  "liked": false,
  "like_count": 1
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 좋아요 등록 }

**POST** `/posts/{post_id}/likes`

로그인한 사용자가 특정 게시글에 좋아요를 등록하거나 유지하기 위한 리소스이다. 요청 처리 결과로 현재 좋아요 여부와 총 좋아요 개수를 response body로 반환하여, 클라이언트가 상태를 즉시 반영할 수 있도록 한다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 로그인 한 사용자만 좋아요를 누를 수 있습니다. Bearer 토큰 인증이 필요합니다. |

**Response (201 Created)** 

```json
{
	"liked": true,
	"like_count": 1
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 댓글 삭제 }

**DELETE** `/posts/{post_id}/comments/{comment_id}`

본인이 작성한 댓글만 삭제하는 리소스입니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 본인이 작성한 댓글만 삭제가 가능해야하므로 Bearer 토큰 인증이 필요합니다. |

**Response (204** No Content**)** 

```json
204 No Content
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 댓글 수정 }

**PATCH** `/posts/{post_id}/comments/{comment_id}`

본인 작성 댓글만 수정이 가능한 리소스입니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 본인이 작성한 댓글에 대한 수정만 가능하도록 해야하므로 Bearer 토큰 인증이 필요합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | O | 내가 작성했던 댓글에 내용을 수정합니다. |

**Request Example** 

```json
{
  "comment": "다시 생각해보니 내 말이 틀렸던 것 같다."
}
```

**Response (200 OK)** 

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "comment": "다시 생각해보니 내 말이 틀렸던 것 같다."
    "updated_at": "2026-01-04T12:00:00Z"
  }
}
```

Response (400 Bad Request) - 필수 입력값 누락

```json
{
  "status": "fail",
  "message": "수정할 댓글 내용을 작성해주세요."
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 댓글 작성 }

**POST** `/posts/{post_id}/comments`

게시글에 댓글을 작성합니다. (로그인 필요)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 댓글을 작성할때 로그인이 필요하다는 요구사항이 있으므로 Bearer 토큰 인증이 필요합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| comment | string | O | 사용자는 게시물에 댓글을 작성할 수 있습니다.(50자 이내) |

**Request Example**

```json
{
  "comment": "정말 웃겨요"
}
```

**Response (201 Created)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "comment": "정말 웃겨요",
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

Response (400 Bad Request) - 필수 입력값 누락

```json
{
  "status": "fail",
  "message": "댓글 내용을 작성해주세요."
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 게시글 삭제 }

**DELETE** `/posts/{post_id}` 

본인이 작성한 게시글을 삭제하는 리소스입니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 본인이 작성한 게시글을 삭제하기 위해Bearer 토큰 인증이 필요합니다. |

**Response (**204 No Content**) - 삭제 완료**

```json
204 No Content
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 게시글 수정 }

**PATCH** `/posts/{post_id}`

본인이 작성한 글의 제목과 내용을 수정할 수 있습니다. (로그인 인증 필요)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 본인이 작성한 글만 수정할 수 있으므로 Bearer 토큰 인증이 필요합니다. |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | X | 사용자는 자신이 작성한 게시물의 제목을 바꿀 수 있습니다. |
| content | string | X | 사용자는 자신이 작성한 게시물의 내용을 바꿀 수 있습니다. |

**Request Example** 

```json
{
  "title": "열심히 하는 개발자는 무조건 성공한다.",
  "content": "취업이 안되는 개발자는 열심히 안한 개발자다."
}
```

**Response (200 OK)**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "열심히 하는 개발자는 무조건 성공한다.",
    "content": "취업이 안되는 개발자는 열심히 안한 개발자다.",
    "updated_at": "2026-01-07T12:00:00Z"
  }
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 게시글 작성 }

POST `/posts`

사용자가 게시글의 제목과 내용을 입력하고 게시글을 작성할 수 있습니다.(반드시 로그인이 필요합니다.)

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 로그인된 회원만 게시글 작성을 할 수있으므로 Bearer 토큰 인증이 필요합니다. |
| Content-Type | string | O | `application/json` → JSON으로 파싱 |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| title | string | O | 사용자가 게시글의 제목을 작성합니다. |
| content | string | O | 사용자가 게시글의 내용을 작성합니다. |

**Request Example**

```json
{
  "title": "개발자는 왜 힘든가?",
  "content": "개발자는 공부를 많이 해야해서 힘들다."
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "개발자는 왜 힘든가?",
    "content": "개발자는 공부를 많이 해야해서 힘들다.",
    "created_at": "2026-01-07T12:00:00Z"
  }
}
```

Response (400 Bad Request) - 필수 입력값 누락

```json
{
  "status": "fail",
  "message": "제목과 내용은 필수 입력 사항 입니다."
}
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 회원 탈퇴 }

**DELETE** `/users/me`

계정을 삭제합니다.

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| **Authorization** | string | O | 회원 탈퇴는 반드시 인증 후 해야하므로 Bearer 토큰 인증이 필요함 |

**Response (**204 No Content**) - 삭제 완료**

```json
204 No Content
```

Response(401 Unauthorized) - 유효하지 않은 토큰이거나 형식이 잘못된 경우

```json
{
  "status": "fail",
  "message": "인증 정보가 올바르지 않습니다. 다시 로그인해 주세요."
}
```

---

### { 프로필 수정 }

**PATCH** `/users/me`

닉네임, 프로필 이미지, 비밀번호 변경

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | `application/json` → JSON으로 파싱 |
| **Authorization** | string | O | 회원 탈퇴는 반드시 인증 후 해야하므로 Bearer 토큰 인증이 필요함 |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| new_nickname | string | X | 사용자가 새로운 닉네임을 설정합니다. |
| new_profile_image | string | X | 새로운 프로필 사진을 넣거나 기존에 있던 프로필 사진을 수정합니다.(5MB)이하 |
| new_password | string | X | 비밀번호 변경을 위해 현재 비밀번호를 요구한뒤 새로운 비밀번호를 입력합니다. |
| current_password | string | X | 보안을 위해 현재 비밀번호를 입력합니다. |

**Request Example** 

```json
{
  "new_nickname": "욱정선",
  "new_profile_image": "https://newimage.com/images/profile.png",
  "current_password" : "123456",
  "new_password": "1234"
}
```

**Response (200 OK)** 

```json
{
  "status": "success",
  "message": "프로필 수정이 완료되었습니다.",
  "data": {
	  "nickname": "욱정선",
	  "profile_image": "https://newimage.com/images/profile.png"
  }
}

```

Response (401 Unauthorized) - 현재 비밀번호가 일치하지 않을 때

```json
{
  "status": "fail",
  "message": "현재 비밀번호가 일치하지 않습니다."
}
```

Response (409 Conflict) - 전과 같은 비밀번호로 변경하려고 할 때

```json
{
  "status": "fail",
  "message": "새 비밀번호가 현재 비밀번호와 같습니다."
}
```

---

### { 로그인 }

**POST** `/auth/token`

사용자 인증 후 액세스 토큰을 발급함. 로그인은 "토큰 리소스 생성"으로 모델링

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | `application/json` → JSON으로 파싱 |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 회원가입한 이메일을 입력합니다. |
| password | string | O | 회원가입한 비밀번호를 입력합니다. |

**Request Example**

```json
{
  "email": "seonjeongug2@gmail.com",
  "password": "123456"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "access_token": "eyASDASFQWFF",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

Response (400 Bad Request)

```json
{
  "status": "fail",
  "message": "email,password은 필수 입력 사항입니다."
}
```

Response (401 Unauthorized)

```json
{
  "status": "fail",
  "message": "아이디 또는 비밀번호가 올바르지 않습니다."
}
```

---

### { 회원가입 }

**POST** `/users`

**회원가입**: 이메일, 비밀번호, 닉네임, 프로필 이미지(선택)로 가입

**Request Headers**

| 헤더 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| Content-Type | string | O | `application/json` → JSON으로 파싱 |

**Request Body**

| 필드 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| email | string | O | 사용자의 이메일을 입력받는다(15자 이내,중복허용) |
| password | string | O | 숫자,특수문자를 포함한 비밀번호(20자 이내) |
| nickname | string | O | 사용자 닉네임(중복 가능) |
| profile_image | string | X | 사용자 프로필 사진(선택, 5MB 이하) |

**Request Example → Reqeust Body 가 있는 경우 작성 필**

```json
{
  "email": "seonjeongug2@gmail.com",
  "password": "123456",
  "nickname": "정정욱",
  "profile_image" : "https://example.com/images/profile.png"
}
```

**Response (201 Created)** 

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "email": "seonjeongug2@gmail.com",
    "nickname": "정정욱",
    "profile_image": "https://example.com/images/profile.png"
    "created_at": "2026-01-04T12:00:00Z"
  }
}
```

Response (400 Bad Request)

```json
{
  "status": "fail",
  "message": "email,password,nickname은 필수 입력 사항입니다."
}
```

---