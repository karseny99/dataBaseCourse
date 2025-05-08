--------------------------- BTREE ------------------------------
-- -- --
EXPLAIN ANALYZE SELECT (*) 
FROM works 
WHERE published_year 
BETWEEN 2010 AND 2017;
-- -- --

Seq Scan on works  (cost=0.00..2350845.88 rows=2419226 width=713) (actual time=19.508..18145.228 rows=2428980 loops=1)
  Filter: ((published_year >= 2010) AND (published_year <= 2017))
  Rows Removed by Filter: 19544013
Planning Time: 1.030 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.323 ms, Inlining 1.149 ms, Optimization 10.881 ms, Emission 6.957 ms, Total 19.310 ms
Execution Time: 18206.079 ms




-- -- --
CREATE INDEX idx_works_published_year_btree ON works(published_year);
-- -- --

Seq Scan on works  (cost=0.00..2350845.88 rows=2419226 width=713) (actual time=28.694..11628.317 rows=2428980 loops=1)
  Filter: ((published_year >= 2010) AND (published_year <= 2017))
  Rows Removed by Filter: 19544013
Planning Time: 1.154 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 1.602 ms, Inlining 2.274 ms, Optimization 12.940 ms, Emission 10.126 ms, Total 26.942 ms
Execution Time: 11683.073 ms


-- -- --
SET enable_seqscan = OFF;
-- -- --


Bitmap Heap Scan on works  (cost=33653.84..2484127.72 rows=2468820 width=712) (actual time=218.556..3187.508 rows=2428980 loops=1)
  Recheck Cond: ((published_year >= 2010) AND (published_year <= 2017))
  Rows Removed by Index Recheck: 594252
  Heap Blocks: exact=32730 lossy=264908
  ->  Bitmap Index Scan on idx_works_published_year_btree  (cost=0.00..33036.64 rows=2468820 width=0) (actual time=196.004..196.004 rows=2428980 loops=1)
        Index Cond: ((published_year >= 2010) AND (published_year <= 2017))
Planning Time: 9.128 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.226 ms, Inlining 1.935 ms, Optimization 10.997 ms, Emission 5.965 ms, Total 19.123 ms
Execution Time: 3234.880 ms






-- -- --
EXPLAIN ANALYZE 
SELECT key, title, published_year -- taking only 2 fields
FROM works 
WHERE published_year BETWEEN 2010 AND 2017;
-- -- -- 

Seq Scan on works  (cost=0.00..2351209.12 rows=2468820 width=60) (actual time=31.884..13715.928 rows=2428980 loops=1)
  Filter: ((published_year >= 2010) AND (published_year <= 2017))
  Rows Removed by Filter: 19544013
Planning Time: 0.051 ms
JIT:
  Functions: 4
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.266 ms, Inlining 1.428 ms, Optimization 17.231 ms, Emission 10.676 ms, Total 29.600 ms
Execution Time: 13780.831 ms





-- -- --
SET enable_seqscan = OFF;
EXPLAIN ANALYZE 
SELECT key, title, published_year 
FROM works 
WHERE published_year BETWEEN 2010 AND 2017;
-- -- -- 


Bitmap Heap Scan on works  (cost=33653.84..2484127.72 rows=2468820 width=60) (actual time=78.550..735.295 rows=2428980 loops=1)
  Recheck Cond: ((published_year >= 2010) AND (published_year <= 2017))
  Rows Removed by Index Recheck: 594252
  Heap Blocks: exact=32730 lossy=264908
  ->  Bitmap Index Scan on idx_works_published_year_btree  (cost=0.00..33036.64 rows=2468820 width=0) (actual time=45.705..45.705 rows=2428980 loops=1)
        Index Cond: ((published_year >= 2010) AND (published_year <= 2017))
Planning Time: 0.044 ms
JIT:
  Functions: 4
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.204 ms, Inlining 1.100 ms, Optimization 17.200 ms, Emission 11.223 ms, Total 29.727 ms
Execution Time: 778.890 ms





-- -- --
EXPLAIN ANALYZE 
SELECT key, title, published_year 
FROM works 
WHERE published_year BETWEEN 2010 AND 2017
order by key desc;
-- -- --

Gather Merge  (cost=2339815.89..2579856.81 rows=2057350 width=60) (actual time=21222.409..22358.843 rows=2428980 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Sort  (cost=2338815.87..2341387.55 rows=1028675 width=60) (actual time=21208.197..21454.421 rows=809660 loops=3)
        Sort Key: key DESC
        Sort Method: external merge  Disk: 59312kB
        Worker 0:  Sort Method: external merge  Disk: 59616kB
        Worker 1:  Sort Method: external merge  Disk: 59072kB
        ->  Parallel Seq Scan on works  (cost=0.00..2158733.55 rows=1028675 width=60) (actual time=47.684..19228.637 rows=809660 loops=3)
              Filter: ((published_year >= 2010) AND (published_year <= 2017))
              Rows Removed by Filter: 6514671
Planning Time: 0.064 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.665 ms, Inlining 47.725 ms, Optimization 50.790 ms, Emission 33.891 ms, Total 133.070 ms
Execution Time: 22408.743 ms



-- -- --
SET enable_seqscan = OFF;
EXPLAIN ANALYZE 
SELECT key, title, published_year 
FROM works 
WHERE published_year BETWEEN 2010 AND 2017
order by key desc;
-- -- --


Gather Merge  (cost=2476387.53..2716428.45 rows=2057350 width=60) (actual time=2746.342..3811.756 rows=2428980 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Sort  (cost=2475387.50..2477959.19 rows=1028675 width=60) (actual time=2723.147..2926.191 rows=809660 loops=3)
        Sort Key: key DESC
        Sort Method: external merge  Disk: 59408kB
        Worker 0:  Sort Method: external merge  Disk: 60304kB
        Worker 1:  Sort Method: external merge  Disk: 58264kB
        ->  Parallel Bitmap Heap Scan on works  (cost=33653.84..2295305.19 rows=1028675 width=60) (actual time=96.157..731.483 rows=809660 loops=3)
              Recheck Cond: ((published_year >= 2010) AND (published_year <= 2017))
              Rows Removed by Index Recheck: 198084
              Heap Blocks: exact=10718 lossy=90109
              ->  Bitmap Index Scan on idx_works_published_year_btree  (cost=0.00..33036.64 rows=2468820 width=0) (actual time=63.905..63.905 rows=2428980 loops=1)
                    Index Cond: ((published_year >= 2010) AND (published_year <= 2017))
Planning Time: 0.072 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.668 ms, Inlining 46.991 ms, Optimization 51.162 ms, Emission 34.591 ms, Total 133.411 ms
Execution Time: 3861.768 ms








-- -- -- 
explain analyze
select key, name
from authors 
where name = 'Kenneth R. Gray'
-- -- -- 


Gather  (cost=1000.00..949394.62 rows=2 width=40) (actual time=28.613..562.441 rows=2 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Parallel Seq Scan on authors  (cost=0.00..948394.42 rows=1 width=40) (actual time=359.459..552.273 rows=1 loops=3)
        Filter: ((name)::text = 'Kenneth R. Gray'::text)
        Rows Removed by Filter: 4712473
Planning Time: 0.056 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.565 ms, Inlining 53.310 ms, Optimization 47.932 ms, Emission 31.693 ms, Total 133.501 ms
Execution Time: 562.722 ms



-- -- -- 
CREATE INDEX idx_authors_name ON authors(name);
explain analyze
select key, name
from authors 
where name = 'Leonard Cyril James McNae'
-- -- -- 

Index Scan using idx_authors_name on authors  (cost=0.56..12.59 rows=2 width=40) (actual time=0.608..0.609 rows=1 loops=1)
  Index Cond: ((name)::text = 'Leonard Cyril James McNae'::text)
Planning Time: 9.171 ms
Execution Time: 0.779 ms





--------------------------- GIN ------------------------------


-- -- --
EXPLAIN ANALYZE
SELECT * 
FROM works 
WHERE works."data" @> '{"title": "Residential Microgrids and Rural Electrifications"}';
-- -- --


Seq Scan on works  (cost=10000000000.00..10002295913.40 rows=2197 width=712) (actual time=14583.212..14583.253 rows=1 loops=1)
  Filter: (data @> '{"title": "Residential Microgrids and Rural Electrifications"}'::jsonb)
  Rows Removed by Filter: 21972992
Planning Time: 0.272 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.131 ms, Inlining 1.627 ms, Optimization 9.617 ms, Emission 4.863 ms, Total 16.239 ms
Execution Time: 14583.423 ms



-- -- --
CREATE INDEX idx_works_data ON works USING gin(data);
-- -- --

Bitmap Heap Scan on works  (cost=10000000085.03..10000008679.34 rows=2197 width=712) (actual time=58.345..58.347 rows=1 loops=1)
  Recheck Cond: (data @> '{"title": "Residential Microgrids and Rural Electrifications"}'::jsonb)
  Heap Blocks: exact=1
  ->  Bitmap Index Scan on idx_works_data  (cost=0.00..84.48 rows=2197 width=0) (actual time=0.357..0.357 rows=1 loops=1)
        Index Cond: (data @> '{"title": "Residential Microgrids and Rural Electrifications"}'::jsonb)
Planning Time: 2.798 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 5.932 ms, Inlining 6.403 ms, Optimization 30.581 ms, Emission 20.845 ms, Total 63.760 ms
Execution Time: 65.126 ms




----------------------------- BRIN ------------------------------------


-- -- --
EXPLAIN ANALYZE
SELECT * FROM works 
WHERE published_year BETWEEN 2010 AND 2017
ORDER BY published_year;
-- -- --


Index Scan using idx_works_published_year_btree on works  (cost=0.44..6388725.67 rows=2466102 width=712) (actual time=0.558..6265.101 rows=2428980 loops=1)
  Index Cond: ((published_year >= 2010) AND (published_year <= 2017))
Planning Time: 0.072 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.458 ms, Inlining 0.000 ms, Optimization 0.000 ms, Emission 0.000 ms, Total 0.458 ms
Execution Time: 6317.695 ms


-- btree off

Sort  (cost=10004296067.85..10004300718.80 rows=1860380 width=712) (actual time=78385.077..78641.481 rows=1818026 loops=1)
  Sort Key: published_year
  Sort Method: external merge  Disk: 1321288kB
  ->  Bitmap Heap Scan on works  (cost=10000000742.13..10002347323.63 rows=1860380 width=712) (actual time=108.195..76899.499 rows=1818026 loops=1)
        Recheck Cond: ((published_year >= 2011) AND (published_year <= 2017))
        Rows Removed by Index Recheck: 15261767
        Heap Blocks: lossy=1569411
        ->  Bitmap Index Scan on idx_works_published_year_brin  (cost=0.00..277.04 rows=4436815 width=0) (actual time=49.103..49.103 rows=15694110 loops=1)
              Index Cond: ((published_year >= 2011) AND (published_year <= 2017))
Planning Time: 0.098 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.185 ms, Inlining 7.146 ms, Optimization 28.861 ms, Emission 22.291 ms, Total 58.483 ms
Execution Time: 78755.930 ms


-- btree & brin off

Sort  (cost=10004299590.09..10004304241.04 rows=1860380 width=712) (actual time=12276.833..12532.901 rows=1818026 loops=1)
  Sort Key: published_year
  Sort Method: external merge  Disk: 1321296kB
  ->  Seq Scan on works  (cost=10000000000.00..10002350845.88 rows=1860380 width=712) (actual time=1003.016..10805.144 rows=1818026 loops=1)
        Filter: ((published_year >= 2011) AND (published_year <= 2017))
        Rows Removed by Filter: 20154967
Planning Time: 0.071 ms
JIT:
  Functions: 2
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.206 ms, Inlining 1.100 ms, Optimization 9.667 ms, Emission 6.032 ms, Total 17.005 ms
Execution Time: 12649.705 ms





-- -- --
EXPLAIN ANALYZE
SELECT * FROM works
WHERE added_at >= NOW() - INTERVAL '1 year'
ORDER BY added_at DESC;
-- -- -- 


Gather Merge  (cost=10002182514.69..10002182723.78 rows=1792 width=712) (actual time=18230.024..18237.756 rows=0 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Sort  (cost=10002181514.67..10002181516.91 rows=896 width=712) (actual time=18168.763..18168.764 rows=0 loops=3)
        Sort Key: added_at DESC
        Sort Method: quicksort  Memory: 25kB
        Worker 0:  Sort Method: quicksort  Memory: 25kB
        Worker 1:  Sort Method: quicksort  Memory: 25kB
        ->  Parallel Seq Scan on works  (cost=10000000000.00..10002181470.73 rows=896 width=712) (actual time=18168.517..18168.517 rows=0 loops=3)
              Filter: (added_at >= (now() - '1 year'::interval))
              Rows Removed by Filter: 7324331
Planning Time: 0.066 ms
JIT:
  Functions: 6
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.885 ms, Inlining 56.460 ms, Optimization 39.058 ms, Emission 26.812 ms, Total 123.214 ms
Execution Time: 18237.995 ms


-- -- -- 
SET enable_seqscan = OFF;
-- -- -- 


Sort  (cost=10000021798.58..10000021803.95 rows=2150 width=712) (actual time=28.983..28.984 rows=0 loops=1)
  Sort Key: added_at DESC
  Sort Method: quicksort  Memory: 25kB
  ->  Bitmap Heap Scan on works  (cost=10000000239.67..10000021679.57 rows=2150 width=712) (actual time=28.980..28.980 rows=0 loops=1)
        Recheck Cond: (added_at >= (now() - '1 year'::interval))
        ->  Bitmap Index Scan on idx_works_added_at_brin  (cost=0.00..239.13 rows=5561 width=0) (actual time=28.978..28.979 rows=0 loops=1)
              Index Cond: (added_at >= (now() - '1 year'::interval))
Planning Time: 0.450 ms
JIT:
  Functions: 3
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.954 ms, Inlining 2.141 ms, Optimization 13.286 ms, Emission 8.777 ms, Total 25.157 ms
Execution Time: 29.979 ms






-- -- --
EXPLAIN ANALYZE
SELECT 
  DATE_TRUNC('month', added_at) AS month,
  COUNT(*) AS works_count
FROM works
WHERE added_at >= NOW() - INTERVAL '3 years'
GROUP BY month
ORDER BY month;
-- -- --


Finalize GroupAggregate  (cost=2334040.41..2363474.63 rows=115045 width=16) (actual time=20374.840..20388.029 rows=8 loops=1)
  Group Key: (date_trunc('month'::text, added_at))
  ->  Gather Merge  (cost=2334040.41..2360886.11 rows=230090 width=16) (actual time=20374.823..20388.010 rows=24 loops=1)
        Workers Planned: 2
        Workers Launched: 2
        ->  Sort  (cost=2333040.38..2333328.00 rows=115045 width=16) (actual time=20314.418..20314.420 rows=8 loops=3)
              Sort Key: (date_trunc('month'::text, added_at))
              Sort Method: quicksort  Memory: 25kB
              Worker 0:  Sort Method: quicksort  Memory: 25kB
              Worker 1:  Sort Method: quicksort  Memory: 25kB
              ->  Partial HashAggregate  (cost=2303709.57..2321402.79 rows=115045 width=16) (actual time=20314.244..20314.355 rows=8 loops=3)
                    Group Key: date_trunc('month'::text, added_at)
                    Planned Partitions: 4  Batches: 1  Memory Usage: 1561kB
                    Worker 0:  Batches: 1  Memory Usage: 1561kB
                    Worker 1:  Batches: 1  Memory Usage: 1561kB
                    ->  Parallel Seq Scan on works  (cost=0.00..2186672.39 rows=2080661 width=8) (actual time=6320.199..20199.084 rows=1612130 loops=3)
                          Filter: (added_at >= (now() - '3 years'::interval))
                          Rows Removed by Filter: 5712201
Planning Time: 0.070 ms
JIT:
  Functions: 27
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 2.881 ms, Inlining 63.661 ms, Optimization 79.665 ms, Emission 64.290 ms, Total 210.497 ms
Execution Time: 20388.492 ms


-- -- -- 
SET enable_seqscan = OFF;
-- -- -- 

GroupAggregate  (cost=10003108703.49..10003147593.46 rows=115045 width=16) (actual time=2903.298..3291.441 rows=8 loops=1)
  Group Key: (date_trunc('month'::text, added_at))
  ->  Sort  (cost=10003108703.49..10003121187.46 rows=4993588 width=8) (actual time=2885.178..3134.374 rows=4836390 loops=1)
        Sort Key: (date_trunc('month'::text, added_at))
        Sort Method: external merge  Disk: 85240kB
        ->  Bitmap Heap Scan on works  (cost=10000001716.92..10002416576.75 rows=4993588 width=8) (actual time=73.635..2234.083 rows=4836390 loops=1)
              Recheck Cond: (added_at >= (now() - '3 years'::interval))
              Rows Removed by Index Recheck: 3142938
              Heap Blocks: lossy=705536
              ->  Bitmap Index Scan on idx_works_added_at_brin  (cost=0.00..468.53 rows=9979872 width=0) (actual time=73.370..73.370 rows=7055360 loops=1)
                    Index Cond: (added_at >= (now() - '3 years'::interval))
Planning Time: 1.913 ms
JIT:
  Functions: 9
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.298 ms, Inlining 3.506 ms, Optimization 27.830 ms, Emission 23.098 ms, Total 54.733 ms
Execution Time: 3297.488 ms




----------------------------------------- COMPLEX ----------------------------------------

CREATE INDEX idx_authors_name_gin ON authors USING gin(name gin_trgm_ops);
CREATE INDEX idx_authors_created_at_brin ON authors USING brin(created_at);
CREATE INDEX idx_author_works_composite ON author_works(author_key, work_key);
CREATE INDEX idx_ratings_rating_value ON ratings(rating_value);
CREATE INDEX idx_ratings_rating_date_brin ON ratings USING brin(rating_date);
CREATE INDEX idx_ratings_works_key ON ratings(works_key);

EXPLAIN ANALYZE
SELECT 
    a.name AS author_name,
    w.title AS work_title,
    w.published_year,
    AVG(r.rating_value)::numeric(3,1) AS avg_rating,
    COUNT(r.id) AS rating_count
FROM authors a
JOIN author_works aw ON a.key = aw.author_key
JOIN works w ON aw.work_key = w.key
LEFT JOIN ratings r ON w.key = r.works_key
WHERE a.name ILIKE '%stephen%'
  AND w.published_year BETWEEN 2000 AND 2020
  AND (r.rating_date IS NULL OR r.rating_date >= '2010-01-01')
GROUP BY a.name, w.title, w.published_year
ORDER BY avg_rating DESC, w.published_year DESC;




Sort  (cost=1823632.44..1823633.22 rows=310 width=82) (actual time=8489.163..8496.129 rows=65 loops=1)
  Sort Key: ((avg(r.rating_value))::numeric(3,1)) DESC, w.published_year DESC
  Sort Method: quicksort  Memory: 32kB
  ->  Finalize GroupAggregate  (cost=1823493.98..1823619.61 rows=310 width=82) (actual time=8473.283..8496.083 rows=65 loops=1)
        Group Key: a.name, w.title, w.published_year
        Filter: (count(r.id) > 5)
        Rows Removed by Filter: 25186
        ->  Gather Merge  (cost=1823493.98..1823593.25 rows=776 width=102) (actual time=8470.839..8490.127 rows=25393 loops=1)
              Workers Planned: 2
              Workers Launched: 2
              ->  Partial GroupAggregate  (cost=1822493.96..1822503.66 rows=388 width=102) (actual time=8410.113..8412.904 rows=8464 loops=3)
                    Group Key: a.name, w.title, w.published_year
                    ->  Sort  (cost=1822493.96..1822494.93 rows=388 width=70) (actual time=8410.094..8410.592 rows=9317 loops=3)
                          Sort Key: a.name, w.title, w.published_year DESC
                          Sort Method: quicksort  Memory: 1508kB
                          Worker 0:  Sort Method: quicksort  Memory: 1461kB
                          Worker 1:  Sort Method: quicksort  Memory: 1631kB
                          ->  Nested Loop Left Join  (cost=2.11..1822477.27 rows=388 width=70) (actual time=181.385..8395.088 rows=9317 loops=3)
                                Filter: ((r.rating_date IS NULL) OR (r.rating_date >= '2010-01-01'::date))
                                ->  Nested Loop  (cost=1.69..1811820.84 rows=388 width=80) (actual time=181.363..8343.872 rows=8711 loops=3)
                                      ->  Nested Loop  (cost=1.12..1804627.47 rows=980 width=38) (actual time=154.058..2851.577 rows=24944 loops=3)
                                            ->  Parallel Index Scan using cuix_authors_key on authors a  (cost=0.56..1796528.76 rows=589 width=40) (actual time=154.012..2754.613 rows=11192 loops=3)
                                                  Filter: ((name)::text ~~* '%stephen%'::text)
                                                  Rows Removed by Filter: 4701282
                                            ->  Index Only Scan using idx_author_works_composite on author_works aw  (cost=0.56..11.84 rows=191 width=37) (actual time=0.007..0.008 rows=2 loops=33575)
                                                  Index Cond: (author_key = a.key)
                                                  Heap Fetches: 0
                                      ->  Index Scan using cuix_works_key on works w  (cost=0.56..7.34 rows=1 width=60) (actual time=0.220..0.220 rows=0 loops=74833)
                                            Index Cond: (key = aw.work_key)
                                            Filter: ((published_year >= 2009) AND (published_year <= 2017))
                                            Rows Removed by Filter: 1
                                ->  Index Scan using idx_ratings_works_key on ratings r  (cost=0.42..27.38 rows=7 width=30) (actual time=0.005..0.005 rows=0 loops=26133)
                                      Index Cond: (works_key = w.key)


Planning Time: 9.044 ms
JIT:
  Functions: 79
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 3.327 ms, Inlining 73.910 ms, Optimization 223.978 ms, Emission 161.636 ms, Total 462.850 ms
Execution Time: 8497.701 ms





begin;
drop INDEX idx_authors_created_at_brin ;
drop INDEX idx_author_works_composite ;
drop INDEX idx_ratings_rating_value ;
drop  INDEX idx_ratings_rating_date_brin ;
drop INDEX idx_ratings_works_key ;

EXPLAIN ANALYZE
SELECT 
    a.name AS author_name,
    w.title AS work_title,
    w.published_year,
    AVG(r.rating_value)::numeric(3,1) AS avg_rating,
    COUNT(r.id) AS rating_count
FROM authors a
JOIN author_works aw ON a.key = aw.author_key
JOIN works w ON aw.work_key = w.key
LEFT JOIN ratings r ON w.key = r.works_key
WHERE a.name ILIKE '%stephen%'
  AND w.published_year BETWEEN 2009 AND 2017
  AND (r.rating_date IS NULL OR r.rating_date >= '2010-01-01')
GROUP BY a.name, w.title, w.published_year
HAVING COUNT(r.id) > 5
ORDER BY avg_rating DESC, w.published_year DESC;
rollback;




Sort  (cost=10001828444.86..10001828445.64 rows=310 width=82) (actual time=14668.443..14674.616 rows=65 loops=1)
  Sort Key: ((avg(r.rating_value))::numeric(3,1)) DESC, w.published_year DESC
  Sort Method: quicksort  Memory: 32kB
  ->  Finalize GroupAggregate  (cost=10001828306.40..10001828432.04 rows=310 width=82) (actual time=14651.840..14674.586 rows=65 loops=1)
        Group Key: a.name, w.title, w.published_year
        Filter: (count(r.id) > 5)
        Rows Removed by Filter: 25186
        ->  Gather Merge  (cost=10001828306.40..10001828405.67 rows=776 width=102) (actual time=14649.118..14668.604 rows=25727 loops=1)
              Workers Planned: 2
              Workers Launched: 2
              ->  Partial GroupAggregate  (cost=10001827306.38..10001827316.08 rows=388 width=102) (actual time=14594.816..14597.600 rows=8576 loops=3)
                    Group Key: a.name, w.title, w.published_year
                    ->  Sort  (cost=10001827306.38..10001827307.35 rows=388 width=70) (actual time=14594.794..14595.273 rows=9317 loops=3)
                          Sort Key: a.name, w.title, w.published_year DESC
                          Sort Method: quicksort  Memory: 1603kB
                          Worker 0:  Sort Method: quicksort  Memory: 1601kB
                          Worker 1:  Sort Method: quicksort  Memory: 1203kB
                          ->  Parallel Hash Left Join  (cost=10000011487.76..10001827289.69 rows=388 width=70) (actual time=14576.386..14582.583 rows=9317 loops=3)
                                Hash Cond: (w.key = r.works_key)
                                Filter: ((r.rating_date IS NULL) OR (r.rating_date >= '2010-01-01'::date))
                                ->  Nested Loop  (cost=1.69..1814166.84 rows=388 width=80) (actual time=32.386..14366.322 rows=8711 loops=3)
                                      ->  Nested Loop  (cost=1.12..1806973.47 rows=980 width=38) (actual time=3.621..9624.206 rows=24944 loops=3)
                                            ->  Parallel Index Scan using pk_author_key on authors a  (cost=0.56..1796528.76 rows=589 width=40) (actual time=3.203..7993.133 rows=11192 loops=3)
                                                  Filter: ((name)::text ~~* '%stephen%'::text)
                                                  Rows Removed by Filter: 4701282
                                            ->  Index Only Scan using pk_authorworks_authorkey_workkey on author_works aw  (cost=0.56..15.82 rows=191 width=37) (actual time=0.142..0.145 rows=2 loops=33575)
                                                  Index Cond: (author_key = a.key)
                                                  Heap Fetches: 0
                                      ->  Index Scan using pk_works_key on works w  (cost=0.56..7.34 rows=1 width=60) (actual time=0.189..0.189 rows=0 loops=74833)
                                            Index Cond: (key = aw.work_key)
                                            Filter: ((published_year >= 2009) AND (published_year <= 2017))
                                            Rows Removed by Filter: 1
                                ->  Parallel Hash  (cost=10000007642.59..10000007642.59 rows=198759 width=30) (actual time=200.070..200.070 rows=159007 loops=3)
                                      Buckets: 65536  Batches: 16  Memory Usage: 2528kB
                                      ->  Parallel Seq Scan on ratings r  (cost=10000000000.00..10000007642.59 rows=198759 width=30) (actual time=154.867..177.826 rows=159007 loops=3)
Planning Time: 5.626 ms
JIT:
  Functions: 88
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 5.164 ms, Inlining 73.088 ms, Optimization 225.278 ms, Emission 166.075 ms, Total 469.606 ms
Execution Time: 14675.484 ms






EXPLAIN ANALYZE
SELECT 
    a.name AS author_name,
    COUNT(DISTINCT w.key) AS works_count,
    COUNT(r.id) AS total_ratings,
    AVG(r.rating_value)::numeric(3,1) AS avg_rating,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY r.rating_value) AS median_rating
FROM authors a
JOIN author_works aw ON a.key = aw.author_key
JOIN works w ON aw.work_key = w.key
JOIN ratings r ON w.key = r.works_key
WHERE r.rating_date BETWEEN '2015-01-01' AND '2022-12-31'
  AND w.published_year >= 1990
GROUP BY a.name
ORDER BY total_ratings DESC, avg_rating DESC;




Sort  (cost=2838716.34..2840261.28 rows=617979 width=56) (actual time=20846.953..21071.100 rows=57427 loops=1)
  Sort Key: (count(r.id)) DESC, ((avg(r.rating_value))::numeric(3,1)) DESC
  Sort Method: external merge  Disk: 3448kB
  ->  GroupAggregate  (cost=2666094.76..2758152.91 rows=617979 width=56) (actual time=20666.168..21049.116 rows=57427 loops=1)
        Group Key: a.name
        ->  Gather Merge  (cost=2666094.76..2738068.59 rows=617979 width=46) (actual time=20665.692..20945.801 rows=200427 loops=1)
              Workers Planned: 2
              Workers Launched: 2
              ->  Sort  (cost=2665094.73..2665738.46 rows=257491 width=46) (actual time=20657.074..20663.515 rows=66809 loops=3)
                    Sort Key: a.name
                    Sort Method: external merge  Disk: 3464kB
                    Worker 0:  Sort Method: external merge  Disk: 3424kB
                    Worker 1:  Sort Method: external merge  Disk: 3584kB
                    ->  Parallel Hash Join  (cost=1947413.61..2634029.81 rows=257491 width=46) (actual time=20431.317..20616.597 rows=66809 loops=3)
                          Hash Cond: (aw.author_key = a.key)
                          ->  Parallel Hash Join  (cost=894104.29..1529495.57 rows=257491 width=45) (actual time=10895.358..11243.798 rows=66809 loops=3)
                                Hash Cond: (aw.work_key = w.key)
                                ->  Parallel Seq Scan on author_works aw  (cost=0.00..443945.57 rows=9802857 width=37) (actual time=0.354..3083.670 rows=7842286 loops=3)
                                ->  Parallel Hash  (cost=891670.34..891670.34 rows=114316 width=44) (actual time=7064.099..7064.101 rows=55646 loops=3)
                                      Buckets: 65536  Batches: 8  Memory Usage: 2208kB
                                      ->  Nested Loop  (cost=0.56..891670.34 rows=114316 width=44) (actual time=0.982..7036.044 rows=55646 loops=3)
                                            ->  Parallel Seq Scan on ratings r  (cost=0.00..8636.39 rows=114316 width=26) (actual time=0.257..23.049 rows=91305 loops=3)
                                                  Filter: ((rating_date >= '2015-01-01'::date) AND (rating_date <= '2022-12-31'::date))
                                                  Rows Removed by Filter: 67703
                                            ->  Index Scan using cuix_works_key on works w  (cost=0.56..7.72 rows=1 width=18) (actual time=0.076..0.076 rows=1 loops=273914)
                                                  Index Cond: (key = r.works_key)
                                                  Filter: (published_year >= 1990)
                          ->  Parallel Hash  (cost=933655.93..933655.93 rows=5890592 width=40) (actual time=9150.878..9150.879 rows=4712474 loops=3)
                                Buckets: 65536  Batches: 512  Memory Usage: 2656kB
                                ->  Parallel Seq Scan on authors a  (cost=0.00..933655.93 rows=5890592 width=40) (actual time=137.630..8126.732 rows=4712474 loops=3)
Planning Time: 12.012 ms
JIT:
  Functions: 85
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 1.770 ms, Inlining 99.540 ms, Optimization 184.225 ms, Emission 128.937 ms, Total 414.471 ms
Execution Time: 21122.214 ms





-- seqscan = OFF;



Sort  (cost=4067340.88..4068885.83 rows=617979 width=56) (actual time=5259.616..5370.221 rows=57427 loops=1)
  Sort Key: (count(r.id)) DESC, ((avg(r.rating_value))::numeric(3,1)) DESC
  Sort Method: external merge  Disk: 3448kB
  ->  GroupAggregate  (cost=3894719.30..3986777.45 rows=617979 width=56) (actual time=5087.531..5349.781 rows=57427 loops=1)
        Group Key: a.name
        ->  Gather Merge  (cost=3894719.30..3966693.14 rows=617979 width=46) (actual time=5087.491..5245.946 rows=200427 loops=1)
              Workers Planned: 2
              Workers Launched: 2
              ->  Sort  (cost=3893719.28..3894363.00 rows=257491 width=46) (actual time=5078.478..5085.631 rows=66809 loops=3)
                    Sort Key: a.name
                    Sort Method: external merge  Disk: 3528kB
                    Worker 0:  Sort Method: external merge  Disk: 3528kB
                    Worker 1:  Sort Method: external merge  Disk: 3424kB
                    ->  Nested Loop  (cost=894187.44..3862654.35 rows=257491 width=46) (actual time=2960.592..5025.459 rows=66809 loops=3)
                          ->  Parallel Hash Join  (cost=894186.88..1978995.44 rows=257491 width=45) (actual time=2960.424..3412.253 rows=66809 loops=3)
                                Hash Cond: (aw.work_key = w.key)
                                ->  Parallel Index Only Scan using idx_author_works_composite on author_works aw  (cost=0.56..893363.41 rows=9802857 width=37) (actual time=0.058..1417.621 rows=7842286 loops=3)
                                      Heap Fetches: 0
                                ->  Parallel Hash  (cost=891752.37..891752.37 rows=114316 width=44) (actual time=653.449..653.451 rows=55646 loops=3)
                                      Buckets: 65536  Batches: 8  Memory Usage: 2208kB
                                      ->  Nested Loop  (cost=82.59..891752.37 rows=114316 width=44) (actual time=100.212..642.065 rows=55646 loops=3)
                                            ->  Parallel Bitmap Heap Scan on ratings r  (cost=82.03..8718.42 rows=114316 width=26) (actual time=100.147..113.002 rows=91305 loops=3)
                                                  Recheck Cond: ((rating_date >= '2015-01-01'::date) AND (rating_date <= '2022-12-31'::date))
                                                  Rows Removed by Index Recheck: 67703
                                                  Heap Blocks: lossy=1846
                                                  ->  Bitmap Index Scan on idx_ratings_rating_date_brin  (cost=0.00..13.44 rows=477022 width=0) (actual time=0.337..0.337 rows=56550 loops=1)
                                                        Index Cond: ((rating_date >= '2015-01-01'::date) AND (rating_date <= '2022-12-31'::date))
                                            ->  Index Scan using cuix_works_key on works w  (cost=0.56..7.72 rows=1 width=18) (actual time=0.006..0.006 rows=1 loops=273914)
                                                  Index Cond: (key = r.works_key)
                                                  Filter: (published_year >= 1990)
                          ->  Index Scan using cuix_authors_key on authors a  (cost=0.56..7.32 rows=1 width=40) (actual time=0.024..0.024 rows=1 loops=200427)
                                Index Cond: (key = aw.author_key)
Planning Time: 10.253 ms
JIT:
  Functions: 67
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 1.617 ms, Inlining 61.767 ms, Optimization 135.688 ms, Emission 102.719 ms, Total 301.791 ms
Execution Time: 5372.457 ms



-- bit map scan = off;


Sort  (cost=5669968.44..5671513.39 rows=617979 width=56) (actual time=12939.934..13056.743 rows=57427 loops=1)
  Sort Key: (count(r.id)) DESC, ((avg(r.rating_value))::numeric(3,1)) DESC
  Sort Method: external merge  Disk: 3448kB
  ->  GroupAggregate  (cost=5497346.86..5589405.02 rows=617979 width=56) (actual time=12756.965..13031.656 rows=57427 loops=1)
        Group Key: a.name
        ->  Gather Merge  (cost=5497346.86..5569320.70 rows=617979 width=46) (actual time=12756.928..12923.554 rows=200427 loops=1)
              Workers Planned: 2
              Workers Launched: 2
              ->  Sort  (cost=5496346.84..5496990.57 rows=257491 width=46) (actual time=12738.067..12745.708 rows=66809 loops=3)
                    Sort Key: a.name
                    Sort Method: external merge  Disk: 3432kB
                    Worker 0:  Sort Method: external merge  Disk: 3528kB
                    Worker 1:  Sort Method: external merge  Disk: 3520kB
                    ->  Nested Loop  (cost=2496815.00..5465281.91 rows=257491 width=46) (actual time=7922.658..12681.066 rows=66809 loops=3)
                          ->  Parallel Hash Join  (cost=2496814.44..3581623.00 rows=257491 width=45) (actual time=7922.065..8380.320 rows=66809 loops=3)
                                Hash Cond: (aw.work_key = w.key)
                                ->  Parallel Index Only Scan using idx_author_works_composite on author_works aw  (cost=0.56..893363.41 rows=9802857 width=37) (actual time=0.291..1474.150 rows=7842286 loops=3)
                                      Heap Fetches: 0
                                ->  Parallel Hash  (cost=2494379.93..2494379.93 rows=114316 width=44) (actual time=5548.454..5548.456 rows=55646 loops=3)
                                      Buckets: 65536  Batches: 8  Memory Usage: 2208kB
                                      ->  Nested Loop  (cost=0.98..2494379.93 rows=114316 width=44) (actual time=102.582..5525.014 rows=55646 loops=3)
                                            ->  Parallel Index Scan using idx_ratings_works_key on ratings r  (cost=0.42..1611345.98 rows=114316 width=26) (actual time=102.161..368.832 rows=91305 loops=3)
                                                  Filter: ((rating_date >= '2015-01-01'::date) AND (rating_date <= '2022-12-31'::date))
                                                  Rows Removed by Filter: 67703
                                            ->  Index Scan using cuix_works_key on works w  (cost=0.56..7.72 rows=1 width=18) (actual time=0.056..0.056 rows=1 loops=273914)
                                                  Index Cond: (key = r.works_key)
                                                  Filter: (published_year >= 1990)
                          ->  Index Scan using cuix_authors_key on authors a  (cost=0.56..7.32 rows=1 width=40) (actual time=0.064..0.064 rows=1 loops=200427)
                                Index Cond: (key = aw.author_key)
Planning Time: 5.826 ms
JIT:
  Functions: 67
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 2.406 ms, Inlining 67.269 ms, Optimization 137.968 ms, Emission 100.234 ms, Total 307.877 ms
Execution Time: 13059.082 ms










































CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS pg_bigm;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE INDEX idx_works_title_gin ON works USING gin(title gin_trgm_ops);

CREATE INDEX idx_works_title_trgm ON works USING gin(title gin_trgm_ops);
CREATE INDEX idx_works_title_bigm ON works USING gin(title gin_bigm_ops);


CREATE INDEX idx_authors_name_trgm ON authors USING gin(name gin_trgm_ops);
CREATE INDEX idx_authors_name_bigm ON authors USING gin(name gin_bigm_ops);




CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    -- pgcrypto:
    password_hash TEXT, 
    encrypted_phone BYTEA, 
    credit_card_encrypted BYTEA, 

    full_name TEXT, 
    bio TEXT, 
    search_vector TSVECTOR, 

    register_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_login TIMESTAMPTZ,
    date_of_birth DATE,

    is_active BOOLEAN DEFAULT TRUE,
    account_balance DECIMAL(12,2) DEFAULT 0.00,
    preferences JSONB, 
    security_question_answer TEXT,

    login_count INT DEFAULT 0,
    rating_score NUMERIC(3,1)
);

CREATE INDEX idx_users_full_name_trgm ON users USING gin (full_name gin_trgm_ops);
CREATE INDEX idx_users_full_name_bigm ON users USING gin (full_name gin_bigm_ops);
CREATE INDEX idx_users_bio_trgm ON users USING gin (bio gin_trgm_ops);
CREATE INDEX idx_users_search_vector ON users USING gin (search_vector);
CREATE INDEX idx_users_register_date_brin ON users USING brin (register_date);
CREATE INDEX idx_users_preferences_gin ON users USING gin (preferences);


INSERT INTO users (username, email, encrypted_phone, credit_card_encrypted)
VALUES (
    'test_user', 
    'test@example.com',
    pgp_sym_encrypt('+79991234567', 'secret_key'),
    pgp_sym_encrypt('4111111111111111', 'secret_key')
);

SELECT 
    user_id,
    pgp_sym_decrypt(encrypted_phone::bytea, 'secret_key') AS phone,
    pgp_sym_decrypt(credit_card_encrypted::bytea, 'secret_key') AS card
FROM users
WHERE user_id = 1;









EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY similarity(title, 'Harry Potter') DESC

Sort  (cost=10000008926.84..10000008932.33 rows=2196 width=46) (actual time=424.767..424.830 rows=1748 loops=1)
  Sort Key: (similarity((title)::text, 'Harry Potter'::text)) DESC
  Sort Method: quicksort  Memory: 233kB
  ->  Bitmap Heap Scan on works  (cost=10000000209.02..10000008804.96 rows=2196 width=46) (actual time=200.042..424.205 rows=1748 loops=1)
        Recheck Cond: ((title)::text ~~ '%Harry Potter%'::text)
        Rows Removed by Index Recheck: 62
        Heap Blocks: exact=1717
        ->  Bitmap Index Scan on idx_works_title_trgm  (cost=0.00..208.47 rows=2196 width=0) (actual time=167.732..167.732 rows=1810 loops=1)
              Index Cond: ((title)::text ~~ '%Harry Potter%'::text)
Planning Time: 9.285 ms
JIT:
  Functions: 4
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.275 ms, Inlining 3.063 ms, Optimization 17.875 ms, Emission 10.928 ms, Total 32.141 ms
Execution Time: 425.228 ms


begin;
drop index idx_works_title_trgm;

EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY similarity(title, 'Harry Potter') desc;
rollback;


Sort  (cost=8926.84..8932.33 rows=2196 width=46) (actual time=201.165..201.218 rows=1748 loops=1)
  Sort Key: (similarity((title)::text, 'Harry Potter'::text)) DESC
  Sort Method: quicksort  Memory: 233kB
  ->  Bitmap Heap Scan on works  (cost=209.02..8804.96 rows=2196 width=46) (actual time=193.994..200.928 rows=1748 loops=1)
        Recheck Cond: ((title)::text ~~ '%Harry Potter%'::text)
        Rows Removed by Index Recheck: 62
        Heap Blocks: exact=1717
        ->  Bitmap Index Scan on idx_works_title_gin  (cost=0.00..208.47 rows=2196 width=0) (actual time=193.847..193.848 rows=1810 loops=1)
              Index Cond: ((title)::text ~~ '%Harry Potter%'::text)
Planning Time: 2.183 ms
Execution Time: 201.356 ms


begin;
drop index idx_works_title_trgm;
drop index idx_works_title_gin;
EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY similarity(title, 'Harry Potter') desc;
rollback;


Sort  (cost=8930.84..8936.33 rows=2196 width=46) (actual time=477.544..477.599 rows=1748 loops=1)
  Sort Key: (similarity((title)::text, 'Harry Potter'::text)) DESC
  Sort Method: quicksort  Memory: 233kB
  ->  Bitmap Heap Scan on works  (cost=213.02..8808.96 rows=2196 width=46) (actual time=469.902..477.300 rows=1748 loops=1)
        Recheck Cond: ((title)::text ~~ '%Harry Potter%'::text)
        Rows Removed by Index Recheck: 14
        Heap Blocks: exact=1675
        ->  Bitmap Index Scan on idx_works_title_bigm  (cost=0.00..212.47 rows=2196 width=0) (actual time=469.732..469.732 rows=1762 loops=1)
              Index Cond: ((title)::text ~~ '%Harry Potter%'::text)
Planning Time: 0.582 ms
Execution Time: 477.830 ms


begin;
drop index idx_works_title_trgm;
drop index idx_works_title_gin;
drop index idx_works_title_bigm;
EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY similarity(title, 'Harry Potter') desc;
rollback;


Gather Merge  (cost=2136740.99..2136954.50 rows=1830 width=46) (actual time=22503.229..22511.798 rows=1748 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Sort  (cost=2135740.96..2135743.25 rows=915 width=46) (actual time=22495.783..22495.819 rows=583 loops=3)
        Sort Key: (similarity((title)::text, 'Harry Potter'::text)) DESC
        Sort Method: quicksort  Memory: 88kB
        Worker 0:  Sort Method: quicksort  Memory: 86kB
        Worker 1:  Sort Method: quicksort  Memory: 85kB
        ->  Parallel Seq Scan on works  (cost=0.00..2135695.95 rows=915 width=46) (actual time=540.104..22494.797 rows=583 loops=3)
              Filter: ((title)::text ~~ '%Harry Potter%'::text)
              Rows Removed by Filter: 7323748
Planning Time: 0.256 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.486 ms, Inlining 75.557 ms, Optimization 48.894 ms, Emission 36.217 ms, Total 161.155 ms
Execution Time: 22535.757 ms



EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY title <-> 'Harry Potter' ASC;  -- Используем оператор <-> (меньше значение = лучше совпадение)




Sort  (cost=8926.84..8932.33 rows=2196 width=46) (actual time=262.394..262.444 rows=1748 loops=1)
  Sort Key: (((title)::text <-> 'Harry Potter'::text))
  Sort Method: quicksort  Memory: 233kB
  ->  Bitmap Heap Scan on works  (cost=209.02..8804.96 rows=2196 width=46) (actual time=255.536..262.179 rows=1748 loops=1)
        Recheck Cond: ((title)::text ~~ '%Harry Potter%'::text)
        Rows Removed by Index Recheck: 62
        Heap Blocks: exact=1717
        ->  Bitmap Index Scan on idx_works_title_trgm  (cost=0.00..208.47 rows=2196 width=0) (actual time=255.417..255.418 rows=1810 loops=1)
              Index Cond: ((title)::text ~~ '%Harry Potter%'::text)
Planning Time: 4.693 ms
Execution Time: 262.536 ms


begin;
drop index idx_works_title_trgm;
drop index idx_works_title_gin;

EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY title <-> 'Harry Potter' ASC;  -- Используем оператор <-> (меньше значение = лучше совпадение)
rollback;

Sort  (cost=8930.84..8936.33 rows=2196 width=46) (actual time=681.944..681.995 rows=1748 loops=1)
  Sort Key: (((title)::text <-> 'Harry Potter'::text))
  Sort Method: quicksort  Memory: 233kB
  ->  Bitmap Heap Scan on works  (cost=213.02..8808.96 rows=2196 width=46) (actual time=674.615..681.740 rows=1748 loops=1)
        Recheck Cond: ((title)::text ~~ '%Harry Potter%'::text)
        Rows Removed by Index Recheck: 14
        Heap Blocks: exact=1675
        ->  Bitmap Index Scan on idx_works_title_bigm  (cost=0.00..212.47 rows=2196 width=0) (actual time=674.497..674.497 rows=1762 loops=1)
              Index Cond: ((title)::text ~~ '%Harry Potter%'::text)
Planning Time: 0.095 ms
Execution Time: 682.091 ms


begin;
drop index idx_works_title_trgm;
EXPLAIN ANALYZE
SELECT title, published_year 
FROM works
WHERE title LIKE '%Harry Potter%'
ORDER BY title <-> 'Harry Potter' ASC;  -- Используем оператор <-> (меньше значение = лучше совпадение)
rollback;

Sort  (cost=8926.84..8932.33 rows=2196 width=46) (actual time=262.944..262.990 rows=1748 loops=1)
  Sort Key: (((title)::text <-> 'Harry Potter'::text))
  Sort Method: quicksort  Memory: 233kB
  ->  Bitmap Heap Scan on works  (cost=209.02..8804.96 rows=2196 width=46) (actual time=256.385..262.739 rows=1748 loops=1)
        Recheck Cond: ((title)::text ~~ '%Harry Potter%'::text)
        Rows Removed by Index Recheck: 62
        Heap Blocks: exact=1717
        ->  Bitmap Index Scan on idx_works_title_gin  (cost=0.00..208.47 rows=2196 width=0) (actual time=256.266..256.266 rows=1810 loops=1)
              Index Cond: ((title)::text ~~ '%Harry Potter%'::text)
Planning Time: 0.114 ms
Execution Time: 263.058 ms














EXPLAIN ANALYZE
SELECT name FROM authors
WHERE name <% 'Li'
ORDER BY name <-> 'Li';




Gather Merge  (cost=949411.00..949548.45 rows=1178 width=24) (actual time=13750.631..13757.220 rows=181 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Sort  (cost=948410.98..948412.45 rows=589 width=24) (actual time=13735.506..13735.509 rows=60 loops=3)
        Sort Key: (((name)::text <-> 'Li'::text))
        Sort Method: quicksort  Memory: 28kB
        Worker 0:  Sort Method: quicksort  Memory: 27kB
        Worker 1:  Sort Method: quicksort  Memory: 27kB
        ->  Parallel Seq Scan on authors  (cost=0.00..948383.88 rows=589 width=24) (actual time=469.886..13735.352 rows=60 loops=3)
              Filter: ((name)::text <% 'Li'::text)
              Rows Removed by Filter: 4712414
Planning Time: 0.193 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.554 ms, Inlining 55.100 ms, Optimization 50.776 ms, Emission 32.718 ms, Total 139.148 ms
Execution Time: 13757.434 ms












begin;
SET enable_seqscan = OFF;
drop index idx_authors_name_bigm;
drop index idx_authors_name;
EXPLAIN ANALYZE
SELECT name FROM authors
WHERE name LIKE '%Le%';
rollback;



Gather  (cost=3115185.14..3799563.94 rows=285566 width=20) (actual time=2709.024..3638.588 rows=343278 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Parallel Bitmap Heap Scan on authors  (cost=3114185.14..3770007.34 rows=118986 width=20) (actual time=2702.549..3610.701 rows=114426 loops=3)
        Recheck Cond: ((name)::text ~~ '%Le%'::text)
        Rows Removed by Index Recheck: 4598048
        Heap Blocks: exact=15967 lossy=272720
        ->  Bitmap Index Scan on idx_authors_name_trgm  (cost=0.00..3114113.75 rows=285566 width=0) (actual time=2650.858..2650.858 rows=1546937 loops=1)
              Index Cond: ((name)::text ~~ '%Le%'::text)
Planning Time: 0.571 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.430 ms, Inlining 79.471 ms, Optimization 46.867 ms, Emission 31.799 ms, Total 158.567 ms
Execution Time: 3654.275 ms





begin;
SET enable_seqscan = OFF;
drop index idx_authors_name_trgm;
drop index idx_authors_name;
EXPLAIN ANALYZE
SELECT name FROM authors
WHERE name LIKE '%Le%';
rollback;


Gather  (cost=3645.14..688023.94 rows=285566 width=20) (actual time=69.944..398.769 rows=343278 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Parallel Bitmap Heap Scan on authors  (cost=2645.14..658467.34 rows=118986 width=20) (actual time=79.219..368.915 rows=114426 loops=3)
        Recheck Cond: ((name)::text ~~ '%Le%'::text)
        Rows Removed by Index Recheck: 1239420
        Heap Blocks: exact=11026 lossy=84259
        ->  Bitmap Index Scan on idx_authors_name_bigm  (cost=0.00..2573.75 rows=285566 width=0) (actual time=38.255..38.256 rows=343278 loops=1)
              Index Cond: ((name)::text ~~ '%Le%'::text)
Planning Time: 0.066 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.449 ms, Inlining 51.803 ms, Optimization 48.670 ms, Emission 31.229 ms, Total 132.152 ms
Execution Time: 405.725 ms







begin;
SET enable_seqscan = ON;
--drop index idx_authors_name_trgm;
EXPLAIN ANALYZE
SELECT name FROM authors
WHERE name LIKE '%Lex%';
rollback;


Bitmap Heap Scan on authors  (cost=30.96..5530.26 rows=1414 width=20) (actual time=10.184..165.870 rows=1771 loops=1)
  Recheck Cond: ((name)::text ~~ '%Lex%'::text)
  Rows Removed by Index Recheck: 630014
  Heap Blocks: exact=30411 lossy=36085
  ->  Bitmap Index Scan on idx_authors_name_trgm  (cost=0.00..30.60 rows=1414 width=0) (actual time=7.183..7.184 rows=70844 loops=1)
        Index Cond: ((name)::text ~~ '%Lex%'::text)
Planning Time: 0.128 ms
Execution Time: 165.946 ms



begin;
SET enable_seqscan = ON;
drop index idx_authors_name_trgm;
EXPLAIN ANALYZE
SELECT name FROM authors
WHERE name LIKE '%Lex%';
rollback;


Bitmap Heap Scan on authors  (cost=42.96..5542.26 rows=1414 width=20) (actual time=6.538..13.857 rows=1771 loops=1)
  Recheck Cond: ((name)::text ~~ '%Lex%'::text)
  Rows Removed by Index Recheck: 2167
  Heap Blocks: exact=3826
  ->  Bitmap Index Scan on idx_authors_name_bigm  (cost=0.00..42.60 rows=1414 width=0) (actual time=6.257..6.258 rows=3938 loops=1)
        Index Cond: ((name)::text ~~ '%Lex%'::text)
Planning Time: 0.079 ms
Execution Time: 13.913 ms


begin;
SET enable_seqscan = ON;
drop index idx_authors_name_trgm;
drop index idx_authors_name_bigm;
EXPLAIN ANALYZE
SELECT name FROM authors
WHERE name LIKE '%Lex%';
rollback;


Gather  (cost=1000.00..949523.81 rows=1414 width=20) (actual time=27.338..641.863 rows=1771 loops=1)
  Workers Planned: 2
  Workers Launched: 2
  ->  Parallel Seq Scan on authors  (cost=0.00..948382.41 rows=589 width=20) (actual time=42.630..631.015 rows=590 loops=3)
        Filter: ((name)::text ~~ '%Lex%'::text)
        Rows Removed by Filter: 4711884
Planning Time: 0.064 ms
JIT:
  Functions: 12
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 0.587 ms, Inlining 49.787 ms, Optimization 46.616 ms, Emission 30.833 ms, Total 127.824 ms
Execution Time: 642.212 ms






EXPLAIN ANALYZE
SELECT 
    a.name AS author_name,
    w.title AS work_title,
    w.published_year,
    -- Используем оба метода сравнения для демонстрации
    bigm_similarity(a.name, 'Juan Jose Calvo De Miguel') AS bigm_score,
    similarity(a.name, 'Juan Jose Calvo De Miguel') AS trgm_score,
    -- Рейтинг и дополнительные данные
    COALESCE(AVG(r.rating_value), 0)::numeric(3,1) AS avg_rating,
    COUNT(r.id) AS ratings_count
FROM 
    authors a
    JOIN author_works aw ON a.key = aw.author_key
    JOIN works w ON aw.work_key = w.key
    LEFT JOIN ratings r ON w.key = r.works_key
WHERE 
    -- Комбинируем условия для демонстрации разных методов
    (a.name <% 'Juan Jose Calvo De Miguel' OR  -- pg_bigm
     a.name % 'Juan Jsoe Calvo De Miguel' OR    -- pg_trgm (с опечаткой)
     w.title % 'Las Trse Fechas Del Destino')  -- pg_trgm с опечаткой в названии
    AND w.published_year BETWEEN 2000 AND 2025
GROUP BY 
    a.name, w.title, w.published_year
ORDER BY 
    -- Комбинированная сортировка по релевантности
    (bigm_similarity(a.name, 'Juan Jose Calvo De Miguel') * 0.7 + 
     similarity(w.title, 'Las Trse Fechas Del Destino') * 0.3) DESC,
    avg_rating DESC
LIMIT 20;

Limit  (cost=4388167.82..4388167.87 rows=20 width=98) (actual time=110477.816..110981.713 rows=20 loops=1)
  ->  Sort  (cost=4388167.82..4388185.46 rows=7055 width=98) (actual time=110275.290..110779.186 rows=20 loops=1)
        Sort Key: (((bigm_similarity((a.name)::text, 'Juan Jose Calvo De Miguel'::text) * '0.7'::double precision) + (similarity((w.title)::text, 'Las Trse Fechas Del Destino'::text) * '0.3'::double precision))) DESC, ((COALESCE(avg(r.rating_value), '0'::numeric))::numeric(3,1)) DESC
        Sort Method: top-N heapsort  Memory: 31kB
        ->  Finalize GroupAggregate  (cost=4386925.11..4387980.09 rows=7055 width=98) (actual time=110250.829..110778.743 rows=2899 loops=1)
              Group Key: a.name, w.title, w.published_year
              ->  Gather Merge  (cost=4386925.11..4387677.30 rows=5880 width=102) (actual time=110250.796..110756.267 rows=2941 loops=1)
                    Workers Planned: 2
                    Workers Launched: 2
                    ->  Partial GroupAggregate  (cost=4385925.08..4385998.58 rows=2940 width=102) (actual time=110240.831..110241.163 rows=980 loops=3)
                          Group Key: a.name, w.title, w.published_year
                          ->  Sort  (cost=4385925.08..4385932.43 rows=2940 width=70) (actual time=110240.810..110240.885 rows=991 loops=3)
                                Sort Key: a.name, w.title, w.published_year
                                Sort Method: quicksort  Memory: 169kB
                                Worker 0:  Sort Method: quicksort  Memory: 160kB
                                Worker 1:  Sort Method: quicksort  Memory: 114kB
                                ->  Parallel Hash Left Join  (cost=3436170.27..4385755.71 rows=2940 width=70) (actual time=110229.337..110239.577 rows=991 loops=3)
                                      Hash Cond: (w.key = r.works_key)
                                      ->  Parallel Hash Join  (cost=3424684.19..4370805.76 rows=2940 width=80) (actual time=38169.856..110045.024 rows=991 loops=3)
                                            Hash Cond: (aw.work_key = w.key)
                                            Join Filter: (((a.name)::text <% 'Juan Jose Calvo De Miguel'::text) OR ((a.name)::text % 'Juan Jsoe Calvo De Miguel'::text) OR ((w.title)::text % 'Las Trse Fechas Del Destino'::text))
                                            Rows Removed by Join Filter: 7841295
                                            ->  Parallel Hash Join  (cost=1053309.33..1722178.40 rows=9802857 width=38) (actual time=13356.085..14301.857 rows=7842286 loops=3)
                                                  Hash Cond: (aw.author_key = a.key)
                                                  ->  Parallel Seq Scan on author_works aw  (cost=0.00..443945.57 rows=9802857 width=37) (actual time=0.008..3536.371 rows=7842286 loops=3)
                                                  ->  Parallel Hash  (cost=933655.93..933655.93 rows=5890592 width=40) (actual time=8937.787..8937.788 rows=4712474 loops=3)
                                                        Buckets: 65536  Batches: 512  Memory Usage: 2656kB
                                                        ->  Parallel Seq Scan on authors a  (cost=0.00..933655.93 rows=5890592 width=40) (actual time=0.026..7920.415 rows=4712474 loops=3)
                                            ->  Parallel Hash  (cost=2158582.20..2158582.20 rows=9155413 width=60) (actual time=22548.697..22548.698 rows=7324331 loops=3)
                                                  Buckets: 65536  Batches: 1024  Memory Usage: 2624kB
                                                  ->  Parallel Seq Scan on works w  (cost=0.00..2158582.20 rows=9155413 width=60) (actual time=0.514..20478.779 rows=7324331 loops=3)
                                                        Filter: ((published_year >= 2000) AND (published_year <= 2025))
                                      ->  Parallel Hash  (cost=7642.59..7642.59 rows=198759 width=26) (actual time=178.790..178.791 rows=159007 loops=3)
                                            Buckets: 65536  Batches: 16  Memory Usage: 2496kB
                                            ->  Parallel Seq Scan on ratings r  (cost=0.00..7642.59 rows=198759 width=26) (actual time=115.697..133.986 rows=159007 loops=3)
Planning Time: 3.194 ms
JIT:
  Functions: 112
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 3.416 ms, Inlining 98.659 ms, Optimization 264.526 ms, Emission 186.537 ms, Total 553.139 ms
Execution Time: 110995.545 ms



SET enable_seqscan = OFF;
EXPLAIN ANALYZE
SELECT 
    a.name AS author_name,
    w.title AS work_title,
    w.published_year,
    -- Используем оба метода сравнения для демонстрации
    bigm_similarity(a.name, 'Juan Jose Calvo De Miguel') AS bigm_score,
    similarity(a.name, 'Juan Jose Calvo De Miguel') AS trgm_score,
    -- Рейтинг и дополнительные данные
    COALESCE(AVG(r.rating_value), 0)::numeric(3,1) AS avg_rating,
    COUNT(r.id) AS ratings_count
FROM 
    authors a
    JOIN author_works aw ON a.key = aw.author_key
    JOIN works w ON aw.work_key = w.key
    LEFT JOIN ratings r ON w.key = r.works_key
WHERE 
    -- Комбинируем условия для демонстрации разных методов
    (a.name <% 'Juan Jose Calvo De Miguel' OR  -- pg_bigm
     a.name % 'Juan Jsoe Calvo De Miguel' OR    -- pg_trgm (с опечаткой)
     w.title % 'Las Trse Fechas Del Destino')  -- pg_trgm с опечаткой в названии
    AND w.published_year BETWEEN 2000 AND 2025
GROUP BY 
    a.name, w.title, w.published_year
ORDER BY 
    -- Комбинированная сортировка по релевантности
    (bigm_similarity(a.name, 'Juan Jose Calvo De Miguel') * 0.7 + 
     similarity(w.title, 'Las Trse Fechas Del Destino') * 0.3) DESC,
    avg_rating DESC
LIMIT 20;




Limit  (cost=5645966.55..5645966.60 rows=20 width=98) (actual time=129474.552..129788.552 rows=20 loops=1)
  ->  Sort  (cost=5645966.55..5645984.19 rows=7055 width=98) (actual time=129327.619..129641.618 rows=20 loops=1)
        Sort Key: (((bigm_similarity((a.name)::text, 'Juan Jose Calvo De Miguel'::text) * '0.7'::double precision) + (similarity((w.title)::text, 'Las Trse Fechas Del Destino'::text) * '0.3'::double precision))) DESC, ((COALESCE(avg(r.rating_value), '0'::numeric))::numeric(3,1)) DESC
        Sort Method: top-N heapsort  Memory: 31kB
        ->  Finalize GroupAggregate  (cost=5644723.84..5645778.82 rows=7055 width=98) (actual time=129302.575..129641.177 rows=2899 loops=1)
              Group Key: a.name, w.title, w.published_year
              ->  Gather Merge  (cost=5644723.84..5645476.03 rows=5880 width=102) (actual time=129302.538..129618.833 rows=2940 loops=1)
                    Workers Planned: 2
                    Workers Launched: 2
                    ->  Partial GroupAggregate  (cost=5643723.81..5643797.31 rows=2940 width=102) (actual time=129287.379..129287.703 rows=980 loops=3)
                          Group Key: a.name, w.title, w.published_year
                          ->  Sort  (cost=5643723.81..5643731.16 rows=2940 width=70) (actual time=129287.346..129287.408 rows=991 loops=3)
                                Sort Key: a.name, w.title, w.published_year
                                Sort Method: quicksort  Memory: 128kB
                                Worker 0:  Sort Method: quicksort  Memory: 134kB
                                Worker 1:  Sort Method: quicksort  Memory: 133kB
                                ->  Nested Loop Left Join  (cost=2377554.40..5643554.44 rows=2940 width=70) (actual time=57990.644..129285.209 rows=991 loops=3)
                                      ->  Parallel Hash Join  (cost=2377553.98..5562858.81 rows=2940 width=80) (actual time=57990.380..129191.383 rows=991 loops=3)
                                            Hash Cond: (aw.work_key = w.key)
                                            Join Filter: (((a.name)::text <% 'Juan Jose Calvo De Miguel'::text) OR ((a.name)::text % 'Juan Jsoe Calvo De Miguel'::text) OR ((w.title)::text % 'Las Trse Fechas Del Destino'::text))
                                            Rows Removed by Join Filter: 7841295
                                            ->  Merge Join  (cost=5.52..2908057.85 rows=9802857 width=38) (actual time=2.164..11786.494 rows=7842286 loops=3)
                                                  Merge Cond: (aw.author_key = a.key)
                                                  ->  Parallel Index Only Scan using idx_author_works_composite on author_works aw  (cost=0.56..893363.41 rows=9802857 width=37) (actual time=0.715..935.889 rows=7842286 loops=3)
                                                        Heap Fetches: 0
                                                  ->  Index Scan using cuix_authors_key on authors a  (cost=0.56..1864270.57 rows=14137422 width=40) (actual time=0.862..7458.700 rows=14137345 loops=3)
                                            ->  Parallel Hash  (cost=2164755.79..2164755.79 rows=9155413 width=60) (actual time=44441.230..44441.231 rows=7324331 loops=3)
                                                  Buckets: 65536  Batches: 1024  Memory Usage: 2624kB
                                                  ->  Parallel Bitmap Heap Scan on works w  (cost=6173.59..2164755.79 rows=9155413 width=60) (actual time=148.188..41899.991 rows=7324331 loops=3)
                                                        Recheck Cond: ((published_year >= 2000) AND (published_year <= 2025))
                                                        Heap Blocks: lossy=686515
                                                        ->  Bitmap Index Scan on idx_works_published_year_brin  (cost=0.00..680.34 rows=21972992 width=0) (actual time=54.602..54.603 rows=20212510 loops=1)
                                                              Index Cond: ((published_year >= 2000) AND (published_year <= 2025))
                                      ->  Index Scan using idx_ratings_works_key on ratings r  (cost=0.42..27.38 rows=7 width=26) (actual time=0.091..0.091 rows=0 loops=2973)
                                            Index Cond: (works_key = w.key)
Planning Time: 2.539 ms
JIT:
  Functions: 85
  Options: Inlining true, Optimization true, Expressions true, Deforming true
  Timing: Generation 2.093 ms, Inlining 70.876 ms, Optimization 228.934 ms, Emission 165.739 ms, Total 467.641 ms
Execution Time: 129789.456 ms