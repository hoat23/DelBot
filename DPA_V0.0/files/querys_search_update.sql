USE [Osiptel_Web]
GO

/*UPDATE TABLE*/
UPDATE dbo.cmsContentNu
SET DATA = Cast ( 
	REPLACE(
		Cast (DATA as nvarchar(max)) , 
		'"res_anio":[{"culture":"","seg":"","val":"[]"}]', 
		'"res_anio":[{"culture":"","seg":"","val":"[\"1996\"]"}]'
		)
	AS ntext)
WHERE DATA LIKE '%96-PD/OSIPTEL%'
 AND DATA LIKE '%"res_anio":/[/{"culture":"","seg":"","val":"/[/]"/}/]%' ESCAPE '/'
 AND DATA LIKE '%val":"/[\"PD\"/]"%' ESCAPE '/'
 

/*SHOW 100 DOCUMENTS*/ 
SELECT TOP (100) * FROM [dbo].[cmsContentNu]
ORDER BY [nodeId] DESC


/*SEARCH YEAR VOID IN DOCUMENT*/
SELECT *
FROM [dbo].[cmsContentNu]
WHERE data LIKE '%96-PD/OSIPTEL%'
 AND DATA LIKE '%val":"/[\"PD\"/]"%' ESCAPE '/'

 AND DATA LIKE '%"res_anio":/[/{"culture":"","seg":"","val":"/[/]"/}/]%' ESCAPE '/'

/*
 AND DATA LIKE '%"res_anio":/[/{"culture":"","seg":"","val":"/[\"1996\"/]"/}/]%' ESCAPE '/'
 */

/*UPDATE FIELD <RV> IN TABLE */
UPDATE dbo.cmsContentNu
SET rv = cast(0 as bigint)
WHERE DATA LIKE '%96-PD/OSIPTEL%'
 AND DATA LIKE '%"res_anio":/[/{"culture":"","seg":"","val":"/[\"1996\"/]"/}/]%' ESCAPE '/'
 AND DATA LIKE '%val":"/[\"PD\"/]"%' ESCAPE '/'
 


/* and nodeId like 26289 */
/*"res_anio":[{"culture":"","seg":"","val":"[]"}]*/
/*'%OSIPTEL%'*/
/*'%001-2007-PD%' */
/*'%2019-PD%'*/