--
-- PostgreSQL database dump
--

\restrict bQEm0nThHuJzmvmAfu2FbPXeWbhofQRWopMnoNnZtazcXtGKiAjUmBz7eJmiosq

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 16.15 (Debian 16.15-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: g2p_intake_form_cultivation_clusters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.g2p_intake_form_cultivation_clusters (
    submission_id uuid NOT NULL,
    application_reference character varying,
    internal_record_id character varying NOT NULL,
    functional_record_id character varying,
    link_internal_record_id character varying,
    link_foundational_id character varying,
    record_name character varying,
    record_image_document_id text,
    created_by character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    last_approved_at timestamp without time zone NOT NULL,
    last_approved_by character varying NOT NULL,
    search_text text,
    record_status character varying NOT NULL,
    record_status_reason character varying,
    latitude character varying,
    longitude character varying,
    altitude character varying,
    plus_code character varying,
    address_line_1 character varying,
    address_line_2 character varying,
    postal_code character varying,
    country_code character varying,
    geo_lowest_level_value_id character varying,
    geo_code_hierarchy_json jsonb,
    land_id character varying,
    is_land_registered boolean,
    land_area numeric,
    cluster_name character varying,
    agro_ecological_zone character varying,
    season character varying,
    cluster_area_hectare numeric,
    number_of_smallholders integer,
    collected_land numeric,
    collected_quintal numeric,
    water_source character varying,
    is_plot_not_registered boolean,
    temporary_land_id character varying,
    sync_id character varying,
    start_gc date,
    start_month integer,
    start_day integer,
    end_gc date,
    end_month integer,
    end_day integer,
    cluster_id character varying,
    cluster_area_timad numeric,
    gps_location character varying,
    cluster_plan numeric,
    cluster_collected_land numeric,
    collected_by_combiner numeric,
    actual_cluster_plan numeric,
    actual_cluster_collected_land numeric,
    actual_cluster_collected_quintal numeric,
    actual_cluster_participant_farmers integer,
    actual_collected_land numeric,
    actual_collected_land_quintal numeric,
    actual_collected_by_combiner numeric,
    is_actual boolean,
    da_name character varying,
    da_mobile_number character varying,
    supervisor_name character varying,
    supervisor_mobile_number character varying,
    water_source_method character varying,
    water_source_frequency character varying,
    region character varying,
    zone character varying,
    woreda character varying,
    kebele character varying,
    sub_kebele character varying
);


ALTER TABLE public.g2p_intake_form_cultivation_clusters OWNER TO postgres;

--
-- Name: g2p_register_cultivation_clusters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.g2p_register_cultivation_clusters (
    internal_record_id character varying NOT NULL,
    functional_record_id character varying,
    link_internal_record_id character varying,
    link_foundational_id character varying,
    record_name character varying,
    record_image_document_id text,
    created_by character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    last_approved_at timestamp without time zone NOT NULL,
    last_approved_by character varying NOT NULL,
    search_text text,
    record_status character varying NOT NULL,
    record_status_reason character varying,
    latitude character varying,
    longitude character varying,
    altitude character varying,
    plus_code character varying,
    address_line_1 character varying,
    address_line_2 character varying,
    postal_code character varying,
    country_code character varying,
    geo_lowest_level_value_id character varying,
    geo_code_hierarchy_json jsonb,
    land_id character varying,
    is_land_registered boolean,
    land_area numeric,
    cluster_name character varying,
    agro_ecological_zone character varying,
    season character varying,
    cluster_area_hectare numeric,
    number_of_smallholders integer,
    collected_land numeric,
    collected_quintal numeric,
    water_source character varying,
    is_plot_not_registered boolean,
    temporary_land_id character varying,
    sync_id character varying,
    start_gc date,
    start_month integer,
    start_day integer,
    end_gc date,
    end_month integer,
    end_day integer,
    cluster_id character varying,
    cluster_area_timad numeric,
    gps_location character varying,
    cluster_plan numeric,
    cluster_collected_land numeric,
    collected_by_combiner numeric,
    actual_cluster_plan numeric,
    actual_cluster_collected_land numeric,
    actual_cluster_collected_quintal numeric,
    actual_cluster_participant_farmers integer,
    actual_collected_land numeric,
    actual_collected_land_quintal numeric,
    actual_collected_by_combiner numeric,
    is_actual boolean,
    da_name character varying,
    da_mobile_number character varying,
    supervisor_name character varying,
    supervisor_mobile_number character varying,
    water_source_method character varying,
    water_source_frequency character varying,
    region character varying,
    zone character varying,
    woreda character varying,
    kebele character varying,
    sub_kebele character varying
);


ALTER TABLE public.g2p_register_cultivation_clusters OWNER TO postgres;

--
-- Name: g2p_register_history_cultivation_clusters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.g2p_register_history_cultivation_clusters (
    history_record_id character varying NOT NULL,
    internal_record_id character varying NOT NULL,
    tab_id character varying NOT NULL,
    section_id character varying NOT NULL,
    change_request_id character varying,
    submission_id character varying,
    change_request_source character varying NOT NULL,
    is_primary_section boolean NOT NULL,
    functional_record_id character varying,
    link_internal_record_id character varying,
    link_foundational_id character varying,
    record_name character varying,
    record_image_document_id text,
    record_status character varying NOT NULL,
    record_status_reason character varying,
    created_by character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    approved_by character varying NOT NULL,
    approved_at timestamp without time zone NOT NULL,
    latitude character varying,
    longitude character varying,
    altitude character varying,
    plus_code character varying,
    address_line_1 character varying,
    address_line_2 character varying,
    postal_code character varying,
    country_code character varying,
    geo_lowest_level_value_id character varying,
    geo_code_hierarchy_json jsonb,
    land_id character varying,
    is_land_registered boolean,
    land_area numeric,
    cluster_name character varying,
    agro_ecological_zone character varying,
    season character varying,
    cluster_area_hectare numeric,
    number_of_smallholders integer,
    collected_land numeric,
    collected_quintal numeric,
    water_source character varying,
    is_plot_not_registered boolean,
    temporary_land_id character varying,
    sync_id character varying,
    start_gc date,
    start_month integer,
    start_day integer,
    end_gc date,
    end_month integer,
    end_day integer,
    cluster_id character varying,
    cluster_area_timad numeric,
    gps_location character varying,
    cluster_plan numeric,
    cluster_collected_land numeric,
    collected_by_combiner numeric,
    actual_cluster_plan numeric,
    actual_cluster_collected_land numeric,
    actual_cluster_collected_quintal numeric,
    actual_cluster_participant_farmers integer,
    actual_collected_land numeric,
    actual_collected_land_quintal numeric,
    actual_collected_by_combiner numeric,
    is_actual boolean,
    da_name character varying,
    da_mobile_number character varying,
    supervisor_name character varying,
    supervisor_mobile_number character varying,
    water_source_method character varying,
    water_source_frequency character varying,
    region character varying,
    zone character varying,
    woreda character varying,
    kebele character varying,
    sub_kebele character varying
);


ALTER TABLE public.g2p_register_history_cultivation_clusters OWNER TO postgres;

--
-- Name: g2p_intake_form_cultivation_clusters g2p_intake_form_cultivation_clusters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.g2p_intake_form_cultivation_clusters
    ADD CONSTRAINT g2p_intake_form_cultivation_clusters_pkey PRIMARY KEY (submission_id, internal_record_id);


--
-- Name: g2p_register_cultivation_clusters g2p_register_cultivation_clusters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.g2p_register_cultivation_clusters
    ADD CONSTRAINT g2p_register_cultivation_clusters_pkey PRIMARY KEY (internal_record_id);


--
-- Name: g2p_register_history_cultivation_clusters g2p_register_history_cultivation_clusters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.g2p_register_history_cultivation_clusters
    ADD CONSTRAINT g2p_register_history_cultivation_clusters_pkey PRIMARY KEY (history_record_id);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_application_reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_application_reference ON public.g2p_intake_form_cultivation_clusters USING btree (application_reference);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_country_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_country_code ON public.g2p_intake_form_cultivation_clusters USING btree (country_code);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_functional_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_g2p_intake_form_cultivation_clusters_functional_record_id ON public.g2p_intake_form_cultivation_clusters USING btree (functional_record_id);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_geo_lowest_level_value_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_geo_lowest_level_value_id ON public.g2p_intake_form_cultivation_clusters USING btree (geo_lowest_level_value_id);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_link_foundational_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_link_foundational_id ON public.g2p_intake_form_cultivation_clusters USING btree (link_foundational_id);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_link_internal_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_link_internal_record_id ON public.g2p_intake_form_cultivation_clusters USING btree (link_internal_record_id);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_plus_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_plus_code ON public.g2p_intake_form_cultivation_clusters USING btree (plus_code);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_postal_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_postal_code ON public.g2p_intake_form_cultivation_clusters USING btree (postal_code);


--
-- Name: ix_g2p_intake_form_cultivation_clusters_sync_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_intake_form_cultivation_clusters_sync_id ON public.g2p_intake_form_cultivation_clusters USING btree (sync_id);


--
-- Name: ix_g2p_register_cultivation_clusters_country_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_country_code ON public.g2p_register_cultivation_clusters USING btree (country_code);


--
-- Name: ix_g2p_register_cultivation_clusters_functional_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_g2p_register_cultivation_clusters_functional_record_id ON public.g2p_register_cultivation_clusters USING btree (functional_record_id);


--
-- Name: ix_g2p_register_cultivation_clusters_geo_lowest_level_value_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_geo_lowest_level_value_id ON public.g2p_register_cultivation_clusters USING btree (geo_lowest_level_value_id);


--
-- Name: ix_g2p_register_cultivation_clusters_link_foundational_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_link_foundational_id ON public.g2p_register_cultivation_clusters USING btree (link_foundational_id);


--
-- Name: ix_g2p_register_cultivation_clusters_link_internal_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_link_internal_record_id ON public.g2p_register_cultivation_clusters USING btree (link_internal_record_id);


--
-- Name: ix_g2p_register_cultivation_clusters_plus_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_plus_code ON public.g2p_register_cultivation_clusters USING btree (plus_code);


--
-- Name: ix_g2p_register_cultivation_clusters_postal_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_postal_code ON public.g2p_register_cultivation_clusters USING btree (postal_code);


--
-- Name: ix_g2p_register_cultivation_clusters_sync_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_cultivation_clusters_sync_id ON public.g2p_register_cultivation_clusters USING btree (sync_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_functional_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_functional_record_id ON public.g2p_register_history_cultivation_clusters USING btree (functional_record_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_internal_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_internal_record_id ON public.g2p_register_history_cultivation_clusters USING btree (internal_record_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_link_foundational_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_link_foundational_id ON public.g2p_register_history_cultivation_clusters USING btree (link_foundational_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_link_internal_record_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_link_internal_record_id ON public.g2p_register_history_cultivation_clusters USING btree (link_internal_record_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_section_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_section_id ON public.g2p_register_history_cultivation_clusters USING btree (section_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_submission_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_submission_id ON public.g2p_register_history_cultivation_clusters USING btree (submission_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_sync_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_sync_id ON public.g2p_register_history_cultivation_clusters USING btree (sync_id);


--
-- Name: ix_g2p_register_history_cultivation_clusters_tab_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_g2p_register_history_cultivation_clusters_tab_id ON public.g2p_register_history_cultivation_clusters USING btree (tab_id);


--
-- PostgreSQL database dump complete
--

\unrestrict bQEm0nThHuJzmvmAfu2FbPXeWbhofQRWopMnoNnZtazcXtGKiAjUmBz7eJmiosq

