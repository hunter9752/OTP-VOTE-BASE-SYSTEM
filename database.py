import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config
from datetime import datetime

class Database:
    def __init__(self):
        self.connection_string = Config.DATABASE_URL
        
    def get_connection(self):
        """Create and return a database connection"""
        return psycopg2.connect(self.connection_string, cursor_factory=RealDictCursor)
    
    def init_db(self):
        """Initialize database tables and insert default candidates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Create voters table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS voters (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    has_voted BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create candidates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS candidates (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    party VARCHAR(255) NOT NULL UNIQUE,
                    votes INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create votes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votes (
                    id SERIAL PRIMARY KEY,
                    voter_email VARCHAR(255) NOT NULL,
                    candidate_id INTEGER REFERENCES candidates(id),
                    voted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert default candidates if they don't exist
            candidates = [
                ('BJP', 'Bharatiya Janata Party'),
                ('Congress', 'Indian National Congress'),
                ('AAP', 'Aam Aadmi Party'),
                ('NOTA', 'None of the Above')
            ]
            
            for party_code, party_name in candidates:
                cursor.execute("""
                    INSERT INTO candidates (name, party)
                    VALUES (%s, %s)
                    ON CONFLICT (party) DO NOTHING
                """, (party_name, party_code))
            
            conn.commit()
            print("✅ Database tables initialized successfully!")
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error initializing database: {e}")
            raise
        finally:
            cursor.close()
            conn.close()
    
    def save_voter(self, name, email):
        """Save or update voter information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO voters (name, email)
                VALUES (%s, %s)
                ON CONFLICT (email) 
                DO UPDATE SET name = EXCLUDED.name
                RETURNING id
            """, (name, email))
            
            voter_id = cursor.fetchone()['id']
            conn.commit()
            return voter_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def get_voter_by_email(self, email):
        """Get voter information by email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM voters WHERE email = %s", (email,))
            voter = cursor.fetchone()
            return voter
        finally:
            cursor.close()
            conn.close()
    
    def check_if_voted(self, email):
        """Check if voter has already voted"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT has_voted FROM voters WHERE email = %s", (email,))
            result = cursor.fetchone()
            return result['has_voted'] if result else False
        finally:
            cursor.close()
            conn.close()
    
    def record_vote(self, email, candidate_id):
        """Record a vote for a candidate"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if already voted
            if self.check_if_voted(email):
                return False, "You have already voted!"
            
            # Record the vote
            cursor.execute("""
                INSERT INTO votes (voter_email, candidate_id)
                VALUES (%s, %s)
            """, (email, candidate_id))
            
            # Update candidate vote count
            cursor.execute("""
                UPDATE candidates 
                SET votes = votes + 1 
                WHERE id = %s
            """, (candidate_id,))
            
            # Mark voter as voted
            cursor.execute("""
                UPDATE voters 
                SET has_voted = TRUE 
                WHERE email = %s
            """, (email,))
            
            conn.commit()
            return True, "Vote recorded successfully!"
            
        except Exception as e:
            conn.rollback()
            return False, f"Error recording vote: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def get_candidates(self):
        """Get all candidates"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM candidates ORDER BY id")
            candidates = cursor.fetchall()
            return candidates
        finally:
            cursor.close()
            conn.close()
    
    def get_results(self):
        """Get voting results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, party, votes 
                FROM candidates 
                ORDER BY votes DESC
            """)
            results = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(*) as total FROM votes")
            total_votes = cursor.fetchone()['total']
            
            return results, total_votes
        finally:
            cursor.close()
            conn.close()

# Initialize database on import
db = Database()
