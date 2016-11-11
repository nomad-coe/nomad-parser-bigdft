package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object BigDFTParserSpec extends Specification {
  "BigDFTParserTest" >> {
    "test with json-events" >> {
      ParserRun.parse(BigDFTParser, "parsers/big-dft/test/examples/single_point/output.out", "json-events") must_== ParseResult.ParseSuccess
    V}
  }

  "test single_point with json" >> {
    ParserRun.parse(BigDFTParser, "parsers/big-dft/test/examples/single_point/output.out", "json") must_== ParseResult.ParseSuccess
  }
}
