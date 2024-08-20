-- Get photometry data for a given image
SELECT
    run.id run_id,
    run.name run_name,
	image.target_name target_name,
    image.filename image_filename,
    image.band band,
    image.exptime exptime,
    image.type image_type,
    parameter.hmin hmin,
    parameter.fmin fmin,
    result.q q,
    result.m_inst m_inst,
    result.m_cte_corr m_cte_corr,
    result.w_cte_pixa_corr_zp w_cte_pixa_corr_zp
FROM run
    LEFT JOIN image ON image.filename = run.image_filename
    LEFT JOIN parameter ON run.parameter_id = parameter.id
    LEFT JOIN result ON run.id = result.run_id
WHERE image.filename LIKE 'ifb444kiq%'


-- Get summary photometry for hmin=3, fmin<3000, quality flag q>0 and q<0.2
SELECT
    run.id run_id,
	image.target_name target_name,
    image.filename image_filename,
    image.band band,
    image.exptime exptime,
    image.type image_type,
    parameter.hmin hmin,
    parameter.fmin fmin,
    AVG(result.q) avg_q,
    MIN(result.m_inst) min_m_inst,
	AVG(result.m_inst) avg_m_inst,
	MAX(result.m_inst) max_m_inst,
	MIN(result.w_cte_pixa_corr_zp) min_w_cte_pixa_corr_zp,
	AVG(result.w_cte_pixa_corr_zp) avg_w_cte_pixa_corr_zp,
	MAX(result.w_cte_pixa_corr_zp) max_w_cte_pixa_corr_zp,
	COUNT() n_objects
FROM run
    LEFT JOIN image ON image.filename = run.image_filename
    LEFT JOIN parameter ON run.parameter_id = parameter.id
    LEFT JOIN result ON run.id = result.run_id
WHERE  result.q > 0 AND result.q < 0.2 AND parameter.hmin = 3 AND parameter.fmin < 3000
GROUP BY 1, 2, 3, 4, 5, 6, 7, 8
ORDER BY 3, 4, 5, 6, 7, 8