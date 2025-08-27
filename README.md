# viral-marketing
viral marketing team project
<img width="3709" height="3840" alt="Mermaid Chart - Create complex, visual diagrams with text  A smarter way of creating diagrams -2025-08-27-025346" src="https://github.com/user-attachments/assets/58db45cf-030e-477f-ace4-63a60bd0c73a" />

---

### 테이블 정의

---

### `users`

* **설명**: 서비스 사용자의 기본 정보를 저장
* **필드**:
    * `email` (VARCHAR, PK, **UNIQUE KEY**): 사용자 이메일 (기본키)
    * `password` (VARCHAR): 해시된 비밀번호
    * `nickname` (VARCHAR, UNIQUE KEY): 사용자 닉네임
    * `name` (VARCHAR): 실명
    * `phone_number` (VARCHAR, UNIQUE KEY): 전화번호
    * `role` (VARCHAR, NOT NULL, DEFAULT 'user'): 사용자 역할 (`admin`, `staff`, `user` 등)
    * `last_logged_in_at` (TIMESTAMP): 마지막 로그인 시각
    * `is_active` (BOOLEAN, NOT NULL, DEFAULT TRUE): 계정 활성화 여부
    * `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP): 계정 생성 시각
    * `deleted_at` (TIMESTAMP): 소프트 삭제 시각 (삭제된 경우)

### `accounts`

* **설명**: 사용자의 계좌 정보를 저장
* **필드**:
    * `account_id` (VARCHAR, PK): 계좌 고유 식별자 (기본키)
    * `user_id` (VARCHAR, FK): 사용자 ID (users 테이블의 email 필드 참조)
    * `account_number` (VARCHAR, UNIQUE KEY): 계좌번호
    * `bank_code` (VARCHAR): 은행 코드 (예: `004` - 국민은행)
    * `account_type` (VARCHAR): 계좌 종류 (`checking`, `savings` 등)
    * `balance` (DECIMAL(19, 4)): 계좌 잔액
    * `currency` (VARCHAR, NOT NULL, DEFAULT 'KRW'): 화폐 단위

---

### `transaction_history`

* **설명**: 계좌 거래 내역을 저장
* **필드**:
    * `transaction_id` (VARCHAR, PK): 거래 내역 고유 식별자
    * `account_id` (VARCHAR, FK): 계좌 ID (accounts 테이블의 account_id 필드 참조)
    * `transaction_type` (VARCHAR, NOT NULL): 거래 종류 (`deposit`, `withdrawal`, `transfer`)
    * `amount` (DECIMAL(19, 4), NOT NULL): 거래 금액
    * `balance_after` (DECIMAL(19, 4), NOT NULL): 거래 후 잔액
    * `memo` (VARCHAR): 거래 메모
    * `transaction_time` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP): 거래 발생 시각

---

### `notifications`

* **설명**: 사용자에게 발송되는 알림 정보를 저장
* **필드**:
    * `notification_id` (VARCHAR, PK): 알림 고유 식별자
    * `user_id` (VARCHAR, FK): 사용자 ID (users 테이블의 email 필드 참조)
    * `message_content` (VARCHAR, NOT NULL): 알림 내용
    * `is_read` (BOOLEAN, NOT NULL, DEFAULT FALSE): 알림 확인 여부
    * `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP): 알림 생성 시각

---

### `analysis`

* **설명**: 사용자별 분석 데이터를 저장
* **필드**:
    * `analysis_id` (VARCHAR, PK): 분석 데이터 고유 식별자
    * `user_id` (VARCHAR, FK): 사용자 ID (users 테이블의 email 필드 참조)
    * `type` (VARCHAR): 분석 종류 (`monthly_report`, `spending_analysis` 등)
    * `period` (VARCHAR): 분석 기간
    * `start_date` (DATE): 분석 시작일
    * `end_date` (DATE): 분석 종료일
    * `description` (VARCHAR): 분석 결과 요약
    * `result_image_url` (VARCHAR): 분석 결과 이미지 URL
    * `created_at` (TIMESTAMP, NOT NULL, DEFAULT CURRENT_TIMESTAMP): 분석 생성 시각
    * `updated_at` (TIMESTAMP): 분석 업데이트 시각

### 관계 (Relationships)

* `users`와 `accounts`: **1:N** (한 명의 사용자가 여러 계정을 보유)
* `accounts`와 `transaction_history`: **1:N** (한 계정에 여러 거래 내역)
* `users`와 `notifications`: **1:N** (한 명의 사용자가 여러 알림을 수신
* `users`와 `analysis`: **1:N** (한 명의 사용자에 대해 여러 분석 데이터를 생성)

`DECIMAL` 타입의 정밀도를 명시(`DECIMAL(19, 4)`)하고, 화폐 단위를 추가하여 재무 관련 데이터의 정확도 향상. 또한, 역할 필드를 통합(`role`), 시간 필드명을 더 직관적으로 변경(`last_logged_in_at`), 소프트 삭제를 위한 필드(`deleted_at`)를 추가.
