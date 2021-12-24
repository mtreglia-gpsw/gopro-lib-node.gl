vec4 filter_contrast(vec4 color, vec2 coords, float contrast, float pivot)
{
    vec3 rgb = color.rgb;

    /* remap contrast in [0;2] to polar coordinates (in [0;π/2]) */
    float polar_c = contrast * ngli_pi / 4.0;
    if (abs(polar_c - ngli_pi / 2.0) < 1e-6) /* at contrast=2, strength is infinite */
        return vec4(step(vec3(pivot), rgb), color.a);

    float strength = tan(polar_c);

    /* Flat/linear interpolation */
    vec3 flat_curve = ngli_sat(strength * (rgb - pivot) + pivot);

    vec3 x_toe = rgb / pivot; /* simplification of ngli_linear(0, pivot, rgb) */
    vec3 x_shoulder = ngli_linear(pivot, 1.0, rgb);

    /* f(x) and 1-f(1-x) creates the symmetry we look for between each piecewise curves */
    vec3 toe = mix(vec3(0.0), vec3(pivot), pow(x_toe, vec3(strength)));
    vec3 shoulder = mix(vec3(pivot), vec3(1.0), 1.0 - pow(1.0 - x_shoulder, vec3(strength)));

    /* S-curved interpolation using toe/shoulder around pivot */
    vec3 s_curve = mix(toe, shoulder, vec3(greaterThan(rgb, vec3(pivot))));

    /* Select S-curve when increasing contrast to prevent hard-clipping */
    color.rgb = ngli_sat(contrast > 1.0 ? s_curve : flat_curve);
    return color;
}