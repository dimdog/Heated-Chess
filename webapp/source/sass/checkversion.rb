require 'sass'

module Sass::Script::Functions
  # https://gist.github.com/nex3/8050187
  def gist_nex3_8050187(suffix)
    Sass::Script::String.new(environment.selector.to_s + suffix.value)
  end
  declare :gist_nex3_8050187, [:suffix]
end
