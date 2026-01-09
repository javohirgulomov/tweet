users = """
        CREATE TABLE IF NOT EXISTS users
        (
            id         BIGSERIAL PRIMARY KEY,
            username   VARCHAR(255) NOT NULL,
            email      VARCHAR(255) NOT NULL UNIQUE,
            password   VARCHAR(128) NOT NULL,
            is_login   BOOLEAN   DEFAULT FALSE,
            is_active  BOOLEAN   DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
tweets = """
         CREATE TABLE IF NOT EXISTS tweets
         (
             id         BIGSERIAL PRIMARY KEY,
             user_id    BIGINT REFERENCES users (id) ON DELETE CASCADE,
             tweet      TEXT NOT NULL,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
         );
         """
likes = """
        CREATE TABLE IF NOT EXISTS likes
        (
            id         BIGSERIAL PRIMARY KEY,
            user_id    BIGINT REFERENCES users (id) ON DELETE SET NULL,
            tweet_id   BIGINT REFERENCES tweets (id) ON DELETE SET NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, tweet_id)
        );
        """

codes = """
        CREATE TABLE IF NOT EXISTS codes
        (
            id         BIGSERIAL PRIMARY KEY,
            email      VARCHAR(255) NOT NULL,
            code       VARCHAR(6),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """