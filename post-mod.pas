CONST
    A = 5, B = 10;
VAR
    C, D, E;

PROCEDURE ONE;
    VAR B, C;

    PROCEDURE TWO;
        VAR C, D;
        BEGIN
            IF C = D THEN
                CALL TWO;
            IF A <> D THEN
                CALL ONE;
            FOR B := 1 TO 10 DO
                FOR D := 10 DOWNTO 1 DO
                    WRITE(D);
        END;

    PROCEDURE THREE;
        VAR X, Y, Z, A, B, C;
        BEGIN
            IF C < X THEN
            BEGIN
                CALL THREE;
                CALL ONE;
            END
            ELSE
                REPEAT
                    WRITELN(X,Y,Z);
                    C := C + 1;
                UNTIL C > X;
        END;

    BEGIN
        IF B <= -(5 + C * A) THEN
            B := B + 1;
        CASE B / C OF
            1: C := B;
            A: B := C;
        CEND;
    END;

VAR
    F, G;

BEGIN
    C := +(C + 1);
    CALL ONE;
    WHILE A > A / A DO
        WHILE B >= B DO
            IF ODD E THEN
                E := E - 1;
END.