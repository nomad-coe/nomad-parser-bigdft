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
  mainFileRe = """              Northwest Computational Chemistry Package \(NWChem\) \d+\.\d+
              ------------------------------------------------------


                    Environmental Molecular Sciences Laboratory
                       Pacific Northwest National Laboratory
                                Richland, WA 99352""".r,
  cmd = Seq(DefaultPythonInterpreter.pythonExe(), "${envDir}/parsers/nwchem/parser/parser-nwchem/nwchemparser/scalainterface.py",
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
