CREATE TABLE website_status (
    id UUID NOT NULL,
    url TEXT NOT NULL,
    occured_at TIMESTAMP WITH TIME ZONE NOT NULL,
    response_time BIGINT,
    error_code INT,
    PRIMARY KEY (id)
);