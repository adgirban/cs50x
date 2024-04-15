-- Keep a log of any SQL queries you execute as you solve the mystery.

--Find the crime scene description
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = "Humphrey Street";

--Two events have been talked about. One is related to theft. Other is related to littering.

--Finding the names of witnesses
SELECT name, transcript
FROM interviews
WHERE month = 7 AND day = 28;

--Since witnesses talked about bakery hence narrowing down
SELECT name, transcript
FROM interviews WHERE month = 7 AND day = 28
AND transcript LIKE "%bakery%";

--Witnesses are Ruth, Eugene and Raymond

--Ruth's clue : Thief left the bakery's parking lot around 10 minutes after theft took place
--Checking bakery's footage to identify the names of suspects via their license plates
SELECT name
FROM people
JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
WHERE month = 7 AND day = 28
AND activity = "exit"
AND hour = 10
AND minute >=15
AND minute <=25
ORDER BY minute;

--Suspect List :
--Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey

--Eugene's clue : Early morning saw the theif withdrawing money at the ATM on Leggett Street
--Checking account number of the potential
SELECT account_number, amount
FROM atm_transactions
WHERE month = 7 AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

--Finding names from these account numbers
SELECT name
FROM people
JOIN bank_accounts, atm_transactions
ON atm_transactions.account_number = bank_accounts.account_number
AND bank_accounts.person_id = people.id
WHERE month = 7 AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

--Suspect List:
--Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

--Raymond's Clue : As the thief was leaving, they called for less than a minute and talked about leaving Fiftyville the next day and also asked to purchase flight tickets.
--Now finding airport at Fiftyville
SELECT abbreviation, full_name
FROM airports
WHERE city = "Fiftyville";

--The airport is CSF (Fiftyville Regional Airport)
--Finding all the flights from CSF on July 29

SELECT flights.id, full_name, city, hour, minute
FROM flights
JOIN airports
ON airports.id = flights.destination_airport_id
WHERE origin_airport_id =
(SELECT id FROM airports WHERE city = "Fiftyville")
AND month = 7 AND day = 29
ORDER BY flights.hour, flights.minute;

--There happen to be 5 flights that day but the first flight is at 8:20am from Fiftyville to LaGuardia Airport NYC
--Check all passengers in that flight

SELECT name, passengers.passport_number, passengers.seat
FROM passengers
JOIN flights ON flights.id = passengers.flight_id
JOIN people ON passengers.passport_number = people.passport_number
WHERE month = 7 AND day = 29
AND flights.hour = 8
AND flights.minute = 20;

--Suspect List:
--Doris, Sofia, Bruce, Edward, Kelsey, Taylor, Kenny, Luca

--Checking call records to find out who bought the tickets
--Caller check:
SELECT name, phone_calls.duration
FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.caller
WHERE month = 7 AND day = 28
AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;

--Suspect List:
--Kelsey, Carina, Taylor, Bruce, Diana, Sofia, Benista, Kenny, Kathryn

--Reciever Check:
SELECT name, phone_calls.duration
FROM phone_calls
JOIN people
ON people.phone_number = phone_calls.receiver
WHERE month = 7 AND day = 28
AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;

--Accomplice:
--Larry, Jacqueline, James, Robin, Philip, Melissa, Jack, Anna, Doris, Luca


--Writing down the suspects from each list
--Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey (Parking Lot)
--Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista (ATM)
--Doris, Sofia, Bruce, Edward, Kelsey, Taylor, Kenny, Luca (Passengers)
--Kelsey, Carina, Taylor, Bruce, Diana, Sofia, Benista, Kenny, Kathryn (Caller)

--Removing obvious innocents i.e ones that are not repeated
--Kathryn, Vanessa, Barry, Brooke, Carina, Edward

--Remaining Suspects:
--Bruce, Luca, Sofia, Iman, Diana, Kelsey (Parking Lot)
--Bruce, Diana, Kenny, Iman, Luca, Taylor, Benista (ATM)
--Doris, Sofia, Bruce, Kelsey, Taylor, Kenny, Luca (Passengers)
--Kelsey, Taylor, Bruce, Diana, Sofia, Benista, Kenny (Caller)

--The only suspect present in all 4 situations is Bruce. Therefore, he must be the Thief.
--The flight is going to New York City. Hence, Bruce is escaping to NYC.
--Matching the phone call data the reciver at the other end for Bruce is Robin. So, Robin must be the accomplice.