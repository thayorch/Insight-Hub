-- Create the issues table
CREATE TABLE issues (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  issue text NOT NULL,
  details text NOT NULL,
  location text NOT NULL,
  category text NOT NULL,
  risk_level integer NOT NULL,
  reason text,
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
