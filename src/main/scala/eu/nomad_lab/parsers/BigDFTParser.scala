package eu.nomad_lab.parsers

import eu.{ nomad_lab => lab }
import eu.nomad_lab.DefaultPythonInterpreter
import org.{ json4s => jn }
import scala.collection.breakOut

object BigDFTParser extends SimpleExternalParserGenerator(
  name = "BigDFTParser",
  parserInfo = jn.JObject(
    ("name" -> jn.JString("BigDFTParser")) ::
      ("parserId" -> jn.JString("BigDFTParser" + lab.BigdftVersionInfo.version)) ::
      ("versionInfo" -> jn.JObject(
        ("nomadCoreVersion" -> jn.JObject(lab.NomadCoreVersionInfo.toMap.map {
          case (k, v) => k -> jn.JString(v.toString)
        }(breakOut): List[(String, jn.JString)])) ::
          (lab.BigdftVersionInfo.toMap.map {
            case (key, value) =>
              (key -> jn.JString(value.toString))
          }(breakOut): List[(String, jn.JString)])
      )) :: Nil
  ),
  mainFileTypes = Seq("text/.*"),
  mainFileRe = """---
 Code logo:
   "__________________________________ A fast and precise DFT wavelet code
   |     |     |     |     |     |
   |     |     |     |     |     |      BBBB         i       gggggg
   |_____|_____|_____|_____|_____|     B    B               g
   |     |  :  |  :  |     |     |    B     B        i     g
   |     |-0+--|-0+--|     |     |    B    B         i     g        g
   |_____|__:__|__:__|_____|_____|___ BBBBB          i     g         g
   |  :  |     |     |  :  |     |    B    B         i     g         g
   |--+0-|     |     |-0+--|     |    B     B     iiii     g         g
   |__:__|_____|_____|__:__|_____|    B     B        i      g        g
   |     |  :  |  :  |     |     |    B BBBB        i        g      g
   |     |-0+--|-0+--|     |     |    B        iiiii          gggggg
   |_____|__:__|__:__|_____|_____|__BBBBB
   |     |     |     |  :  |     |                           TTTTTTTTT
   |     |     |     |--+0-|     |  DDDDDD          FFFFF        T
   |_____|_____|_____|__:__|_____| D      D        F        TTTT T
   |     |     |     |  :  |     |D        D      F        T     T
   |     |     |     |--+0-|     |D         D     FFFF     T     T
   |_____|_____|_____|__:__|_____|D___      D     F         T    T
   |     |     |  :  |     |     |D         D     F          TTTTT
   |     |     |--+0-|     |     | D        D     F         T    T
   |_____|_____|__:__|_____|_____|          D     F        T     T
   |     |     |     |     |     |         D               T    T
   |     |     |     |     |     |   DDDDDD       F         TTTT
   |_____|_____|_____|_____|_____|______                    www.bigdft.org   "
""".r,
  cmd = Seq(DefaultPythonInterpreter.pythonExe(), "${envDir}/parsers/big-dft/parser/parser-big-dft/bigdftparser/scalainterface.py",
    "${mainFilePath}"),
  cmdCwd = "${mainFilePath}/..",
  resList = Seq(
    "parser-big-dft/bigdftparser/__init__.py",
    "parser-big-dft/bigdftparser/setup_paths.py",
    "parser-big-dft/bigdftparser/parser.py",
    "parser-big-dft/bigdftparser/scalainterface.py",
    "parser-big-dft/bigdftparser/versions/__init__.py",
    "parser-big-dft/bigdftparser/versions/bigdft180/__init__.py",
    "parser-big-dft/bigdftparser/versions/bigdft180/mainparser.py",
    "nomad_meta_info/public.nomadmetainfo.json",
    "nomad_meta_info/common.nomadmetainfo.json",
    "nomad_meta_info/meta_types.nomadmetainfo.json",
    "nomad_meta_info/big_dft.nomadmetainfo.json"
  ) ++ DefaultPythonInterpreter.commonFiles(),
  dirMap = Map(
    "parser-big-dft" -> "parsers/big-dft/parser/parser-big-dft",
    "nomad_meta_info" -> "nomad-meta-info/meta_info/nomad_meta_info"
  ) ++ DefaultPythonInterpreter.commonDirMapping()
)
