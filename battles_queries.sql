USE battles;

SELECT DISTINCT region
FROM battles_data;


SELECT count(name)
FROM battles_data;

SELECT attacker_king,count(attacker_king) AS most_active_count
FROM battles_data
GROUP BY attacker_king
ORDER BY  COUNT(most_active_count) DESC
LIMIT 1;

SELECT attacker_outcome,count(attacker_outcome) AS most_active_count 
                    FROM battles_data
                    WHERE attacker_outcome = 'loss'
                    GROUP BY attacker_outcome;
                    
SELECT name FROM battLes_data WHERE (attacker_king = 'Stannis Baratheon' OR defender_king = 'Stannis Baratheon')  	;