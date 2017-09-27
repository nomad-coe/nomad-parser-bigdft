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
  mainFileRe = """__________________________________ A fast and precise DFT wavelet code\s*
   \|     \|     \|     \|     \|     \|\s*
   \|     \|     \|     \|     \|     \|      BBBB         i       gggggg\s*
   \|_____\|_____\|_____\|_____\|_____\|     B    B               g\s*
   \|     \|  :  \|  :  \|     \|     \|    B     B        i     g\s*
   \|     \|-0\+--\|-0\+--\|     \|     \|    B    B         i     g        g\s*
   \|_____\|__:__\|__:__\|_____\|_____\|___ BBBBB          i     g         g\s*
   \|  :  \|     \|     \|  :  \|     \|    B    B         i     g         g\s*
   \|--\+0-\|     \|     \|-0\+--\|     \|    B     B     iiii     g         g\s*
   \|__:__\|_____\|_____\|__:__\|_____\|    B     B        i      g        g\s*
   \|     \|  :  \|  :  \|     \|     \|    B BBBB        i        g      g\s*
   \|     \|-0\+--\|-0\+--\|     \|     \|    B        iiiii          gggggg\s*
   \|_____\|__:__\|__:__\|_____\|_____\|__BBBBB\s*
   \|     \|     \|     \|  :  \|     \|                           TTTTTTTTT\s*
   \|     \|     \|     \|--\+0-\|     \|  DDDDDD          FFFFF        T\s*
   \|_____\|_____\|_____\|__:__\|_____\| D      D        F        TTTT T\s*
   \|     \|     \|     \|  :  \|     \|D        D      F        T     T\s*
   \|     \|     \|     \|--\+0-\|     \|D         D     FFFF     T     T\s*
   \|_____\|_____\|_____\|__:__\|_____\|D___      D     F         T    T\s*
   \|     \|     \|  :  \|     \|     \|D         D     F          TTTTT\s*
   \|     \|     \|--\+0-\|     \|     \| D        D     F         T    T\s*
   \|_____\|_____\|__:__\|_____\|_____\|          D     F        T     T\s*
   \|     \|     \|     \|     \|     \|         D               T    T\s*
   \|     \|     \|     \|     \|     \|   DDDDDD       F         TTTT\s*
   \|_____\|_____\|_____\|_____\|_____\|______                    www\.bigdft\.org""".r,
  cmd = Seq(DefaultPythonInterpreter.pythonExe(), "${envDir}/parsers/big-dft/parser/parser-big-dft/bigdftparser/scalainterface.py",
    "${mainFilePath}"),
  cmdCwd = "${mainFilePath}/..",
  resList = Seq(
    "parser-big-dft/bigdftparser/__init__.py",
    "parser-big-dft/bigdftparser/setup_paths.py",
    "parser-big-dft/bigdftparser/parser.py",
    "parser-big-dft/bigdftparser/scalainterface.py",
    "parser-big-dft/bigdftparser/versions/__init__.py",
    "parser-big-dft/bigdftparser/versions/bigdft18/__init__.py",
    "parser-big-dft/bigdftparser/versions/bigdft18/mainparser.py",
    "parser-big-dft/bigdftparser/generic/__init__.py",
    "parser-big-dft/bigdftparser/generic/libxc_codes.py",
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
