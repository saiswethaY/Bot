CREATE TABLE IF NOT EXISTS candidate_profile (
    profile_id BIGSERIAL PRIMARY KEY,
    profile_name VARCHAR(100) NOT NULL,
    experience_min NUMERIC(4,2) NOT NULL,
    experience_max NUMERIC(4,2) NOT NULL,
    notice_period_days INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id BIGSERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    external_job_id VARCHAR(255),
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    location VARCHAR(255),
    experience_min NUMERIC(4,2),
    experience_max NUMERIC(4,2),
    job_url TEXT NOT NULL,
    description TEXT,
    posted_at TIMESTAMP,
    discovered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'FOUND',
    CONSTRAINT uq_source_external_job
        UNIQUE (source, external_job_id)
);

CREATE TABLE IF NOT EXISTS job_matches (
    match_id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    match_score NUMERIC(5,2) NOT NULL,
    matched_skills JSONB,
    missing_skills JSONB,
    match_status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    evaluated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_job_match_job
        FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
    CONSTRAINT fk_job_match_profile
        FOREIGN KEY (profile_id) REFERENCES candidate_profile(profile_id) ON DELETE CASCADE,
    CONSTRAINT uq_job_profile_match
        UNIQUE (job_id, profile_id)
);

CREATE TABLE IF NOT EXISTS applications (
    application_id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL,
    profile_id BIGINT NOT NULL,
    application_status VARCHAR(50) NOT NULL DEFAULT 'READY',
    applied_at TIMESTAMP,
    resume_version VARCHAR(100),
    cover_letter_version VARCHAR(100),
    failure_reason TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_application_job
        FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE,
    CONSTRAINT fk_application_profile
        FOREIGN KEY (profile_id) REFERENCES candidate_profile(profile_id) ON DELETE CASCADE,
    CONSTRAINT uq_application_job_profile
        UNIQUE (job_id, profile_id)
);

CREATE TABLE IF NOT EXISTS application_events (
    event_id BIGSERIAL PRIMARY KEY,
    application_id BIGINT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_message TEXT,
    event_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_application_event
        FOREIGN KEY (application_id)
        REFERENCES applications(application_id)
        ON DELETE CASCADE
);
