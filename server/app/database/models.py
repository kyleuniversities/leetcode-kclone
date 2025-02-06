# Imports
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

# Users Table
class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default='user')

# Problem Set Table
class ProblemSet(Base):
    __tablename__ = 'problem_set'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    public = Column(Boolean, default = True)

# Problem Table
class Problem(Base):
    __tablename__ = 'problem'
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    name = Column(String)
    description_url = Column(String)
    starter_code_url = Column(String)
    author_id = Column(Integer, ForeignKey("user.id"))
    set_id = Column(Integer, ForeignKey("problem_set.id"))

# Test Case Table
class TestCase(Base):
    __tablename__ = 'test_case'
    id = Column(Integer, primary_key=True, index=True)
    time_limit = Column(Integer)
    parameters = Column(String)
    solution = Column(String)
    problem_id = Column(Integer, ForeignKey("problem.id"))

# Submission Set Table
class SubmissionSet(Base):
    __tablename__ = 'submission_set'
    id = Column(Integer, primary_key=True, index=True)
    score_earned = Column(Integer)
    score_possible = Column(Integer)
    time_taken = Column(Integer)
    author_id = Column(Integer, ForeignKey("user.id"))
    problem_set_id = Column(Integer, ForeignKey("problem_set.id"))

# Submission Table
class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True, index=True)
    code_url = Column(String)
    score_earned = Column(Integer)
    score_possible = Column(Integer)
    time_taken = Column(Integer)
    author_id = Column(Integer, ForeignKey("user.id"))
    problem_id = Column(Integer, ForeignKey("problem.id"))
    set_id = Column(Integer, ForeignKey("submission_set.id"))

# Test Case Table
class SubmissionTestCase(Base):
    __tablename__ = 'submission_test_case'
    id = Column(Integer, primary_key=True, index=True)
    success = Column(Boolean)
    submission_id = Column(Integer, ForeignKey("submission.id"))
    test_case_id = Column(Integer, ForeignKey("test_case.id"))
