CREATE PROCEDURE InsertAudioAndRecord
    @file_data VARBINARY(MAX),
    @file_name NVARCHAR(255),
    @is_poss BIT,
    @score DECIMAL(10, 4),
    @full_text NVARCHAR(MAX),
    @main_text NVARCHAR(MAX),
	@tg_id NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;

        INSERT INTO AudioFiles (file_name, file_data)
        VALUES (@file_name, @file_data);

        DECLARE @file_id INT = SCOPE_IDENTITY();

		declare @tgs_id INT=null
		select @tgs_id=id
		from tgs
		where tg_id=@tg_id

		if @tgs_id is null
		begin
			INSERT INTO tgs(tg_id)
			values (@tg_id)
			set @tgs_id = SCOPE_IDENTITY();
		end

        INSERT INTO Records (file_id, is_poss, score, full_text, main_text, tg_id)
        VALUES (@file_id, @is_poss, @score, @full_text, @main_text, @tgs_id);

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;

        THROW;
    END CATCH
END;
