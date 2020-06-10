# more subqueries exercise

2015-10-24

## part 1

Suppliers(**sid: integer**, sname: string, address: string)

Parts(**pid: integer**, pname: string, color: string)

Catalog(**sid: integer, pid: integer**, cost: real)

1. Find the names of suppliers who supply some red part.

		SELECT S.sname
		FROM Suppliers S, Parts P, Catalog C
		WHERE C.pid=P.pid AND C.sid AND P.color='red';

2. Find the sids of suppliers who supply some red or green part.

		select c.sid
		from parts p, catalog c
		where p.pid=c.pid and (p.color='red' or p.color='green')

3. find the sids of suppliers who supply some red part or are at 221 packer street.

		select s.sid
		from suppliers s
		where s.address = '221 packer street' or s.sid in 
			(select c.sid
			 from parts p, catalog c
			 where p.pid=c.pid and p.color='red');

4. find the sids of suppliers who supply some red part and some green part.

		select c.sid
		from catalog c, parts p
		where c.pid=p.pid and p.color='red' and exists
			(select p2.pid
			 from parts p2, catalog c2
			 where p2.color='green' and c2.sid=c.sid and p2.pid=c2.pid);

**5. find the sids of suppliers who supply every part.**

		select c.sid
		from catalog c
		where not exists
			(select p.pid
			 from parts p
			 where not exists
			 	(select c1.sid
			 	 from catalog c1
			 	 where c1.sid=c.sid and c1.pid=p.pid));

**6. find the sids of suppliers who supply every red part.**

		select c.sid
		from catalog c
		where not exists
			(select p.pid
			 from parts p
			 where p.color='red' and not exists
			 	(select c1.sid
			 	 from catalog c1
			 	 where c1.sid=c.sid and c1.pid=p.pid));

**7. find the sids of suppliers who supply every red or green part.**

		select c.sid
		from catalog c
		where not exists
			(select p.pid
			 from parts p
			 where (p.color = 'red' or p.color = 'green') 
			 and (not exists
			 		(select c1.sid
			 		 from catalog c1
			 		 where c1.sid = c.sid and c1.pid = p.pid)));

**8. find the sids of suppliers who supply every red part or supply every green part.**

		select c.sid
		from catalog c
		where not exists
			(select p.pid
			 from parts p
			 where p.color = 'red'
			 and (not exists
			 		(select c1.sid
			 		 from catalog c1
			 		 where c1.sid = c.sid
			 		 and c1.pid = p.pid )));

9. find pairs of sids such that the supplier with the first sid charges more for some part than the supplier with the second sid.

		select c1.sid, c2.sid
		from catalog c1, catalog c2
		where c1.pid = c2.pid and c1.sid <> c2.sid and c1.cost > c2.cost;

10. find the pids of parts supplied by at least two different suppliers.

		select c.pid
		from catalog c
		where exists (select c1.sid
					  from catalog c1
					  where c1.pid = c.pid and c1.sid <> c.sid);

11. find the pids of the most expensive parts supplied by suppliers named Yosemite Sham.

		select c.pid
		from catalog c, suppliers s
		where s.name = 'Yosemite Sham' and c.sid=s.sid
		and c.cost >= all (select c2.cost
						   from catalog c2, suppliers s2
						   where s2.sname = 'Yosemite Sham' and c2.sid = s2.sid)

> 12. find the pids of parts supplied by every supplier at less than $200. (if any supplier either does not supply the part or charge more than $200 for it, the part is not selected)

## part 2

Flights(**flno: integer**, from: string, to: string, distance: integer, departs: time, arrives: time)

Aircraft(**aid: integer**, aname: string, cruisingrange: integer)

Certified(**eid: integer, aid: integer**)

Employees(**eid: integer**, ename: string, salary: integer)

1. find the eids of pilots certified for some Boeing aircraft.

		select c.eid
		from certified c, aircraft a
		where c.aid = a.aid and a.aname = 'Boeing';

2. find the names of pilots certified for some Boeing aircraft.

		select c.eid, e.ename
		from certified c, aircraft a, employees e
		where c.aid = a.aid and a.aname = 'Boeing' and e.eid = c.eid;

3. find the aids of all aircraft that can be used on non-stop flights from Bonn to Madras.

		select a.aid
		from aircraft a, flights f
		where f.from = 'Bonn' and f.to = 'Madras' and a.cruisingrange >= f.distance;

4. identify the flights that can be piloted by every pilot whose salary is more than $100,000.

		select f.flno
		from employees e, certified c, flights f, aircraft a
		where e.eid = c.eid and e.salary > 100,000 and a.aid = c.cid and a.crusingrange > f.distance;

5. find the names of pilots who can operate planes with a range greater than 3,000 miles but are not certified on any Boeing aircraft.

		select e.ename
		from certified c, aircraft a, employees e
		where c.eid = e.eid and c.aid= a.aid and a.cruisingrange > 3000 and c.eid not in (select c2.eid
																						  from certified c2, aircraft a2
																						  where a2.aid = c2.aid and a2.name = 'Boeing');

6. find the eids of employees who make the highest salary.

		select e.eid
		from employees e
		where e.salary = (select max(e2.salary) from employees e2);

7. find the eids of employees who make the second highest salary.

		select e.eid
		from employees e
		where e.salary = (select max(e2.salary)
						  from employees e2
						  where e2.salary <> (select max(e3.salary)
						  					  from employees e3));

**8. find the eids of employees who are certified for the largest number of aircraft.**

		select temp.eid
		from (select c.eid, count(c.aid) as cnt
			  from certified c
			  group by c.eid) as temp
		where temp.cnt = (select max(temp.cnt) from temp);

9. find the eids of employees who are certified for exactly three aircraft.

		select temp.eid
		from (select c.eid, count(c.aid) as cnt
		      from certified c
		      group by c.eid) as temp
		where temp.cnt = 3

10. find the total amount paid to employees as salaries.

		select sum(e.salary) from employees e;

> 11. is there a sequence of flights from Madison to Timbuktu? each flight in the sequence is required to depart from the city that the destination of the previous flight; the first flight must leave Madison, the last flight must reach Timbuktu, and there is no restriction on the number of intermediate flights. your query must determine whether a sequence of flights from Madison to Timbuktu exists for any input Flights relation instance.
