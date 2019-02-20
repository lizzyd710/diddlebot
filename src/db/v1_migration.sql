/* Create the quips table. An ID PK will be handy for these.
 * Quips are effectively unconstrained in size.
 */
CREATE TABLE quips (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  quip TEXT NOT NULL
);

/* Create cancellations table. It seems scandalous to create a date as a text field,
 * but SQLite actually has pretty good, loose date support. See:
 * https://www.sqlite.org/lang_datefunc.html
 */
CREATE TABLE cancellations (
  date DATE NOT NULL UNIQUE
);

/* Attendance record table that tracks individuals missing/arriving late
 * to rehearsal. Again, SQLite dates are stored as text and can be used
 * with these handy functions: https://www.sqlite.org/lang_datefunc.html
 */
CREATE TABLE attendance (
  type TEXT NOT NULL,
  date TEXT NOT NULL,
  name TEXT NOT NULL,
  reason TEXT
);

INSERT INTO quips (quip) VALUES
("Keep your inner beats down!"),
("Your left hand is WRONG!"),
("Get your feet in time"),
("Can you even hear the metronome?"),
("I heard at blue devils they make you good by running laps"),
("NYSPC is rigged"),
("one band ONE SOUND"),
("Listen in!"),
("Battery, stop listening forward!"),
("Beware the DCA Showers"),
("Did we miss the sports fed meeting this week?"),
("BD is a cult"),
("Play until your hands bleed."),
("What would Reuel do?"),
("Sticks out for Harambe"),
("Did Tommy oversleep again?"),
("python sux");
