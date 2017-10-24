from pynodegl import (
        GLBlendState,
        GLState,
        Group,
        Media,
        Program,
        Quad,
        Render,
        Texture2D,
        Triangle,
)

from pynodegl_utils.misc import scene

from OpenGL import GL

fragment="""
#version 100
precision mediump float;
void main() {
    gl_FragColor = vec4(0.0, 0.0, 0.0, 0.5);
}
"""

@scene()
def blending_test(cfg):
    g = Group()
    g2 = Group()

    q = Quad((-0.5, -0.5, 0), (1, 0, 0), (0, 1, 0))
    m = Media(cfg.medias[0].filename)
    t = Texture2D(data_src=m)
    p = Program()
    ts = Render(q, p)
    ts.update_textures(tex0=t)
    g.add_children(ts)

    q = Quad((-0.1, 0.0, 0), (1.1, 0, 0), (0, 1, 0))
    p = Program(fragment=fragment)
    ts = Render(q, p)
    ts.add_glstates(GLBlendState(GL.GL_TRUE,
                                 GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA,
                                 GL.GL_ONE, GL.GL_ZERO))
    g.add_children(ts)

    q = Quad((-1.0, 0.0, 0), (1.1, 0, 0), (0, 1, 0))
    p = Program(fragment=fragment)
    ts = Render(q, p)
    ts.add_glstates(GLBlendState(GL.GL_TRUE,
                                 GL.GL_ONE, GL.GL_ONE_MINUS_SRC_ALPHA,
                                 GL.GL_ONE, GL.GL_ZERO))
    g.add_children(ts)

    q = Quad((-0.125, -0.125, 0), (0.25, 0, 0), (0, 0.25, 0))
    p = Program(fragment=fragment)
    ts = Render(q, p)
    ts.add_glstates(GLBlendState(GL.GL_FALSE))

    g2.add_children(g, ts)

    return g2
