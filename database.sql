-- Create the issues table
CREATE TABLE issues (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  issue text NOT NULL,
  details text NOT NULL,
  location text NOT NULL,
  category text NOT NULL,
  risk_level integer NOT NULL,
  reason text,
  status text NOT NULL DEFAULT 'unresolved' CHECK (status IN ('unresolved', 'in_progress', 'resolved')),
  report_count integer NOT NULL DEFAULT 1,
  assignee text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security (RLS)
ALTER TABLE issues ENABLE ROW LEVEL SECURITY;

-- Allow anonymous inserts (so your backend/users can add reports)
CREATE POLICY "Enable insert for anonymous users" ON issues 
  FOR INSERT WITH CHECK (true);

-- Allow anonymous reads (so the dashboard can display them)
CREATE POLICY "Enable read for anonymous users" ON issues
  FOR SELECT USING (true);

-- Allow anonymous updates (so the dashboard can edit/toggle status/merge duplicates)
CREATE POLICY "Enable update for anonymous users" ON issues
  FOR UPDATE USING (true) WITH CHECK (true);

-- Allow anonymous deletes (so the dashboard can remove records)
CREATE POLICY "Enable delete for anonymous users" ON issues
  FOR DELETE USING (true);

-- Migration: run this if the "issues" table already exists in Supabase
ALTER TABLE issues ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'unresolved';
ALTER TABLE issues ADD CONSTRAINT issues_status_check CHECK (status IN ('unresolved', 'in_progress', 'resolved'));
ALTER TABLE issues ADD COLUMN IF NOT EXISTS report_count integer NOT NULL DEFAULT 1;
ALTER TABLE issues ADD COLUMN IF NOT EXISTS assignee text;
