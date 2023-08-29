import sqlalchemy
# adding employees,name,id,phone,career,salary,photo,department,voulenteer
# adding departments(headquarter,cleaning_centers),name,location
# adding a new deceased name, id,sex,age_type,birthdate,residence,address,deathdatetime,cause_of_date,body_status,center,reporter,witnesses,datetime_of_prayer, time and date was delivered,cemetery,cleaner,datetime_created,datetime_updated 
# adding a reporter name ,id ,phone, address,deceased_relation,
# adding 2 witnesses, ids, phones
# adding cleaners name,id,phone,center_number
# adding centers name,location
# adding mosque name, location
# adding permission,number,target,date
# adding files,title
# adding end_hospital,name,location
# adding a cemetery name, address
# adding a grave, row_number,
# adding a driver name, id,phone,car
# adding a car,company,model,year,color,blates_number,photo
# from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm import declarative_base, relationship

# Base = declarative_base()

# # Employees Table
# class Employee(Base):
#     __tablename__ = 'employees'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     phone = Column(String)
#     career = Column(String)
#     salary = Column(Integer)
#     photo = Column(String)
#     department_id = Column(Integer, ForeignKey('departments.id'))
#     department = relationship("Department")
#     volunteer = Column(String)

# # Departments Table
# class Department(Base):
#     __tablename__ = 'departments'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     location = Column(String)
#     headquarter = Column(String)
#     cleaning_centers = Column(String)

# # Deceased Table
# class Deceased(Base):
#     __tablename__ = 'deceased'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     sex = Column(String)
#     age_type = Column(String)
#     birthdate = Column(DateTime)
#     residence = Column(String)
#     address = Column(String)
#     deathdatetime = Column(DateTime)
#     cause_of_death = Column(String)
#     body_status = Column(String)
#     center_id = Column(Integer, ForeignKey('centers.id'))
#     center = relationship("Center")
#     reporter_id = Column(Integer, ForeignKey('reporters.id'))
#     reporter = relationship("Reporter")
#     witnesses = relationship("Witness", back_populates="deceased")
#     datetime_of_prayer = Column(DateTime)
#     datetime_delivered = Column(DateTime)
#     cemetery_id = Column(Integer, ForeignKey('cemeteries.id'))
#     cemetery = relationship("Cemetery")
#     cleaner_id = Column(Integer, ForeignKey('cleaners.id'))
#     cleaner = relationship("Cleaner")
#     datetime_created = Column(DateTime)
#     datetime_updated = Column(DateTime)

# # Reporter Table
# class Reporter(Base):
#     __tablename__ = 'reporters'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     phone = Column(String)
#     address = Column(String)
#     deceased_relation = Column(String)

# # Witness Table
# class Witness(Base):
#     __tablename__ = 'witnesses'
#     id = Column(Integer, primary_key=True)
#     phone = Column(String)
#     deceased_id = Column(Integer, ForeignKey('deceased.id'))
#     deceased = relationship("Deceased", back_populates="witnesses")

# # Cleaner Table
# class Cleaner(Base):
#     __tablename__ = 'cleaners'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     phone = Column(String)
#     center_number = Column(Integer)

# # Center Table
# class Center(Base):
#     __tablename__ = 'centers'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     location = Column(String)

# # Other Tables (Mosque, Permission, File, EndHospital, Cemetery, Grave, Driver, Car) would be defined similarly.

# # mosque table
# class Mosque(Base):
#     __tablename__ = 'mosque'
#     id = Column(Integer,primary_key=True)
#     name = Column(String)
#     location = Column(String)
# # Create the database engine and tables
# engine = create_engine('sqlite:///your_database.db')
# Base.metadata.create_all(engine)
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String,Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("sqlite:///mydatabase.db", echo=True)
class Base(DeclarativeBase):
    pass

class Employee(Base):
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    phone: Mapped[str] = mapped_column(String)
    career: Mapped[str] = mapped_column(String)
    salary: Mapped[int] = mapped_column(Integer)
    photo: Mapped[str] = mapped_column(String)
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))
    department: Mapped["Department"] = relationship("Department")
    volunteer: Mapped[str] = mapped_column(String)

class Department(Base):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    headquarter: Mapped[str] = mapped_column(String)
    cleaning_centers: Mapped[str] = mapped_column(String)

Base.metadata.create_all(engine)


if __name__ == "__main__":
    # Create a new employee
    new_employee = Employee(name="John", phone="1234567890", career="Manager", salary=50000, photo="photo.jpg", department_id=1, volunteer="Yes")

    # Add the employee to the database
    with Session(engine) as session:
        session.add(new_employee)
        session.commit()

    # Query the database
    with Session(engine) as session:
        employee = session.query(Employee).first()
        print(employee.name, employee.salary)
